from enum import Enum
from typing import Annotated

import typer
from rich.prompt import Prompt
from rich.table import Table
from sqlmodel import Session, select
from typer import Typer

from mydev.agent.models import User, APIKey
from mydev.console import console
from mydev.db import init_db, create_engine
from mydev.utils.secrets import generate_api_key, hash_api_key

db_app = Typer()


class Entity(str, Enum):
    user = "user"
    api_key = "api_key"


@db_app.command(name="ls")
def list_entity(entity: Annotated[Entity, typer.Option(prompt=True)]):
    engine = create_engine()

    if entity == Entity.user:
        with Session(engine) as session:
            statement = select(User)
            users = session.exec(statement)
            table = Table("ID", "Username")
            for user in users:
                table.add_row(str(user.id), user.name)
            console.print(table)
    elif entity == Entity.api_key:
        username = Prompt.ask("Enter username")
        with Session(engine) as session:
            statement = select(User, APIKey).where(User.name == username).where(User.id == APIKey.user_id)
            user_api_keys = session.exec(statement)
            table = Table("ID", "User Name", "Hashed Key")
            for user, api_key in user_api_keys:
                table.add_row(str(api_key.id), user.name, f"{api_key.hashed_key[:8]}...")
            console.print(table)


@db_app.command(name="add")
def create_entity(
    entity: Annotated[Entity, typer.Option(prompt=True)],
    username: Annotated[str, typer.Option(prompt=True)],
):
    engine = create_engine()

    if entity == Entity.user:
        raise NotImplementedError
    elif entity == Entity.api_key:
        with Session(engine) as session:
            statement = select(User).where(User.name == username)
            user = session.exec(statement).first()
            if not user:
                console.print(f"User {username} does not exist")
                return
            api_key_text = generate_api_key()
            hashed_key = hash_api_key(api_key_text)
            api_key = APIKey(user_id=user.id, hashed_key=hashed_key)
            session.add(api_key)
            session.commit()
            session.refresh(api_key)
            console.print(f"Generated API key for user {username}:\n{api_key_text}")


@db_app.command(name="init")
def init():
    init_db()


@db_app.callback(invoke_without_command=True, no_args_is_help=True)
def main():
    pass
