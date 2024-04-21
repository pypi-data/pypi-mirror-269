import getpass
import os
from typing import Optional

import typer
import uvicorn
from sqlmodel import Session, select
from rich.prompt import Prompt

from mydev.agent.models import Agent, SSHConfig
from mydev.config import try_load_config
from mydev.console import console
from mydev.db import create_engine
from mydev.utils.constants import MYDEV_SRC_DIR
from mydev.utils.ssh import load_ssh_config_file, test_ssh_connection

agent_app = typer.Typer()


def _get_ssh_config(alias: str = None, hostname: str = None, pub_key_path: str = "~/.ssh/id_rsa.pub"):
    if hostname is None:
        hostname = os.uname().nodename
    if alias is None:
        alias = hostname
    username = getpass.getuser()
    pub_key_path = os.path.abspath(os.path.expanduser(pub_key_path))
    if not os.path.exists(pub_key_path):
        console.print("SSH public key not found, please generate one first")
        return None
    else:
        with open(pub_key_path, "r") as f:
            pub_key = f.read().strip()
        return SSHConfig(
            alias=alias,
            hostname=hostname,
            username=username,
            pub_key=pub_key,
        )


@agent_app.command(name="launch")
def launch(reload: bool = False, target: str = "local", alias: Optional[str] = None):
    # insert the local agent record into the database
    if target == "local":
        cfg = try_load_config()
        engine = create_engine()
        with Session(engine) as session:
            # check if the agent, which userid is the same and the is local
            statement = select(Agent).where(Agent.user_id == cfg.local_user_id).where(Agent.is_local)
            agent = session.exec(statement).first()
            if agent is None:
                hostname = os.uname().nodename
                ssh_config = _get_ssh_config(alias=alias)
                session.add(ssh_config)
                session.commit()
                session.refresh(ssh_config)
                agent = Agent(
                    user_id=cfg.local_user_id,
                    hostname=hostname,
                    alias=alias if alias is not None else hostname,
                    is_local=True,
                    is_active=True,
                    ssh_config_id=ssh_config.id if ssh_config is not None else None,
                )
            else:
                agent.is_active = True
            session.add(agent)
            session.commit()
            session.refresh(agent)

    # launch fastapi server
    app_dir = os.path.abspath(os.path.join(MYDEV_SRC_DIR, ".."))
    reload_dir = os.path.join(MYDEV_SRC_DIR, "agent")
    uvicorn.run(
        app="mydev.agent.main:app",
        host="127.0.0.1",
        port=8000,
        reload=reload,
        reload_dirs=[reload_dir],
        app_dir=app_dir,
    )


@agent_app.command(name="add")
def add(alias: Optional[str] = None):
    cfg = try_load_config()
    engine = create_engine()

    if os.path.exists(os.path.expanduser("~/.ssh/config")):
        ssh_conf_file = load_ssh_config_file(os.path.expanduser("~/.ssh/config"))
    else:
        ssh_conf_file = None

    ssh_hostname = Prompt.ask("Enter SSH hostname")
    if ssh_hostname in ssh_conf_file.hosts():
        console.print(f"SSH hostname {ssh_hostname} exists in ~/.ssh/config")
        ssh_host = ssh_conf_file.host(ssh_hostname)
        with Session(engine) as session:
            if session.exec(select(Agent).where(Agent.hostname == ssh_hostname).where(Agent.is_local)).first():
                console.print(f"Agent with hostname {ssh_hostname} already exists")
                return

            console.print("testing ssh connection...")
            if test_ssh_connection(ssh_hostname):
                console.print(f"SSH connection to {ssh_hostname} is successful")
            else:
                console.print(f"SSH connection to {ssh_hostname} failed")
                raise NotImplementedError
            from fabric import Connection

            result = Connection(ssh_hostname).run("cat ~/.ssh/id_rsa.pub", hide=True)
            ssh_pub_key = result.stdout.strip()
            if len(ssh_pub_key) == 0:
                ssh_pub_key = None

            ssh_config = SSHConfig(
                alias=alias if alias is not None else ssh_hostname,
                hostname=ssh_host["hostname"],
                username=ssh_host["user"],
                pub_key=ssh_pub_key,
                port=ssh_host.get("port", 22),
            )
            session.add(ssh_config)
            session.commit()
            session.refresh(ssh_config)

            agent = Agent(
                user_id=cfg.local_user_id,
                hostname=ssh_hostname,
                alias=alias if alias is not None else ssh_hostname,
                is_local=True,
                is_active=False,
                ssh_config_id=ssh_config.id if ssh_config is not None else None,
            )
            session.add(agent)
            session.commit()
            session.refresh(agent)

    console.print("Agent added successfully")


@agent_app.callback(invoke_without_command=True, no_args_is_help=True)
def main():
    pass
