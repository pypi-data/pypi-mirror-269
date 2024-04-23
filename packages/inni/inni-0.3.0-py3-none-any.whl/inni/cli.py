import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Any, Optional

import click
from playwright._impl._driver import compute_driver_executable
from rich.console import Console

from inni.config import default_config, read_config
from inni.loader import load_module

console = Console()
error_console = Console(stderr=True, style="red bold")


@click.group()
@click.option(
    "-c", "--config", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.option(
    "-v", "--vars-file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.pass_context
def inni(ctx: click.Context, config: Optional[str], vars_file: Optional[str]):
    ctx.ensure_object(dict)
    if config is None:
        config = str(default_config())
    ctx.obj["config"] = read_config(config)
    if vars_file is not None:
        vars_module: Path = Path(vars_file)
    else:
        vars_module: Path = default_config().parent / "vars.py"

    if vars_module.exists():
        module_dir = vars_module.parent
        sys.path.append(str(module_dir))
        ctx.obj["vars"] = import_module(vars_module.name.removesuffix(".py"))
        sys.path.remove(str(module_dir))


def _login_out(ctx: click.Context, login: bool, override_modules: Optional[str]):
    config = ctx.obj["config"]
    module_names = config["inni"]["login" if login else "logout"]
    if override_modules:
        console.print("[yellow] CLI modules override the modules defined in config")
        module_names = [i.strip() for i in override_modules.split(",")]
    prompts = config["inni"]["prompts"]
    modules = {}

    with console.status("") as status:
        for module_name in module_names:
            status.update(f"[green]Initializing {module_name}")
            try:
                module = load_module(module_name)
                module_config = config["modules"].get(module_name, {})
                modules[module_name] = module(module_config, console, error_console)
            except ModuleNotFoundError as err:
                status.stop()
                error_console.print(err.msg)
                sys.exit(0)
    console.print("[green]✅ Initialized Modules")
    console.print("")

    variables_to_prompt = set()
    for module in modules.values():
        variables_to_prompt.update(
            module.template_variables()["login" if login else "logout"]
        )
    variables_to_prompt -= {"vars"}

    responses: dict[str, Any] = {
        "vars": ctx.obj.get("vars", {}),
    }
    for var in variables_to_prompt:
        prompt = prompts.get(var, f"{var}:").strip() + " "
        responses[var] = console.input("[blue]" + prompt)

    console.print(f"\n[green bold]Logging {'In' if login else 'Out'}\n")
    for name, module in modules.items():
        console.rule(f"[bold cyan]Module: {name}", align="left")
        try:
            if login:
                module.login(responses)
            else:
                module.logout(responses)
        except Exception:
            error_console.print(f"[red bold]Fatal error occured running module {name}")
            error_console.print_exception()


@inni.command()
@click.option("-m", "--modules", help="Modules to run (overrides config modules)")
@click.pass_context
def login(ctx: click.Context, modules: Optional[str] = None):
    """
    Login today

    Runs all the login modules along with prompting for user input
    """
    return _login_out(ctx, True, modules)


@inni.command()
@click.option("-m", "--modules", help="Modules to run (overrides config modules)")
@click.pass_context
def logout(ctx: click.Context, modules: Optional[str] = None):
    """
    Logout today

    Runs all the login modules along with prompting for user input
    """
    return _login_out(ctx, False, modules)


@inni.command()
def download_browser():
    """
    Download Firefox for bitrix module

    Bitrix doesn't provide an API, we emulate clicks in a browser and need an
    instance of firefox for that.
    """
    command = compute_driver_executable()
    subprocess.run([*command, "install", "firefox"])
