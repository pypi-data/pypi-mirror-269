import re
import subprocess

import psutil

from inni.modules.base import BaseModule


class Module(BaseModule):
    login_template_keys = ("login_template",)
    logout_template_keys = ("logout_template",)

    def handle_entry(self, entry):
        if "exec" not in entry:
            name = entry.get("name", "unnamed")
            self.err.print(f"No exec found in {name} entry. Skipping.")
            return

        name = entry.get("name", entry["exec"])
        shell = entry.get("shell", False)

        self.out.print(f"[bold]Entry: {name}")
        if "if_running" in entry:
            regex = re.compile(entry["if_running"])
            for process in self.processes:
                if regex.findall(process):
                    self.out.print("[green]✅ Matching process found.")
                    break
            else:
                self.out.print(
                    "[yellow]✗  No process matching regex found. Skipping entry"
                )
                return

        if "if_not_running" in entry:
            regex = re.compile(entry["if_not_running"])
            for process in self.processes:
                if regex.findall(process):
                    self.out.print(
                        "[yellow]✗  Process matching regex found. Skipping entry"
                    )
                    return
            self.out.print("[green]✅ No such process is running.")

        if "if_true" in entry:
            self.out.print(f"[blue]Running {entry['if_true']}")
            process = subprocess.run(
                entry["if_true"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=shell,
            )
            if process.returncode:
                self.out.print(
                    f"[yellow]✗  Process exited with exit code {process.returncode}. "
                    f"Skipping entry."
                )
                return
            self.out.print("[green]✅ Check process ran as expected.")

        if "if_false" in entry:
            self.out.print(f"[blue]Running {entry['if_false']}")
            process = subprocess.run(
                entry["if_false"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=shell,
            )
            if not process.returncode:
                self.out.print("[yellow]✗  Process ran successfully. Skipping entry")
                return
            self.out.print("[green]✅ Check process failed as expected.")

        self.out.print("[green]✅ Running entry")
        subprocess.Popen(
            entry["exec"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            shell=shell,
        )

    def run_all(self, login: bool):
        entries = self.config.get("login" if login else "logout", [])
        self.processes = [
            " ".join(i.cmdline()) or i.name() for i in psutil.process_iter()
        ]
        for entry in entries:
            self.handle_entry(entry)
            self.out.print()

    def login(self, responses):
        self.run_all(True)

    def logout(self, responses):
        self.run_all(False)
