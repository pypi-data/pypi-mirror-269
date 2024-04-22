from typing import Optional

import typer
from rich.prompt import Prompt

from mydev.cli.agent import agent_app
from mydev.cli.db import db_app
from mydev.cli.infra import infra_app
from mydev.cli.pm import pm_app
from mydev.config import try_load_config, save_config
from mydev.console import console
from mydev.db import create_user, get_user_by_name

app = typer.Typer()
app.add_typer(db_app, name="db")
app.add_typer(agent_app, name="agent")
app.add_typer(pm_app, name="pm")
app.add_typer(infra_app, name="infra")


@app.command(name="config")
def config(username: Optional[str] = None):
    console.print("Configuring MyDev...")
    cfg = try_load_config()

    cfg.username = Prompt.ask("Enter username", default=cfg.username) if username is None else username

    user = get_user_by_name(cfg.username)
    if user is None:
        console.print(f"User {cfg.username} not found, creating new user")
        user = create_user(cfg.username)
    else:
        console.print(f"User {cfg.username} exists")
    cfg.local_user_id = user.id

    console.print(cfg)
    save_config(cfg)
    typer.echo("Configuration saved")


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main():
    pass


def run() -> None:
    """Run commands."""
    app()
