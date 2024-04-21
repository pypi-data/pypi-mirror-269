import typer

from typer import Typer

infra_app = Typer()


@infra_app.command(name="shell")
def shell():
    pass


@infra_app.callback(invoke_without_command=True, no_args_is_help=True)
def main():
    pass
