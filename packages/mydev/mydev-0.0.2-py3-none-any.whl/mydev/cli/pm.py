import shlex
from typing import Optional

import typer
from rich.table import Table

from mydev.console import console

pm_app = typer.Typer()


@pm_app.command(name="ls")
def list_proc():
    from mydev.pm.manager import Manager

    manager = Manager()
    proc_list = manager.list_proc()
    table = Table("ID", "Command", "Status", "Alias")
    for proc in proc_list:
        table.add_row(str(proc.id), proc.cmd, proc.status, proc.alias)
    console.print(table)


@pm_app.command(name="rm")
def remove(proc_id: Optional[int] = None, all: bool = False):
    from mydev.pm.manager import Manager

    manager = Manager()
    if proc_id is not None:
        if manager.remove(proc_id):
            console.print(f"Process {proc_id} removed")
        else:
            console.print(f"Process {proc_id} not found")
    elif all:
        for proc in manager.list_proc():
            manager.remove(proc.id)
        console.print("All processes removed")
    else:
        console.print("Please provide a process ID or use --all flag")


@pm_app.command(name="run")
def run(cmd: list[str], alias: Optional[str] = None):
    from mydev.pm.manager import Manager

    manager = Manager()
    manager.run(shlex.join(cmd), alias)


@pm_app.command(name="kill")
def kill(proc_id: int):
    from mydev.pm.manager import Manager

    manager = Manager()
    manager.kill(proc_id)


@pm_app.command(name="cat")
def cat(proc_id: int):
    from mydev.pm.manager import Manager

    manager = Manager()
    out = manager.cat(proc_id)
    console.print(out)


@pm_app.callback(invoke_without_command=True, no_args_is_help=True)
def main():
    pass
