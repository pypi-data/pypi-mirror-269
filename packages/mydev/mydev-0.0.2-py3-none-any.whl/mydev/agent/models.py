from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)


class APIKey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    hashed_key: str


class GPU(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    agent_id: int | None = Field(default=None, foreign_key="agent.id")

    local_id: int
    gpu_util: int | None = None
    memory_util: int | None = None


class SSHConfig(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

    alias: str
    hostname: str
    username: str
    pub_key: str
    port: int = 22
    sync_to_all: bool = False


class Agent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

    hostname: str
    alias: str
    is_local: bool = False  # only one agent can be local
    is_active: bool = True

    is_controller: bool = False
    controller_id: int | None = None

    cpu_util: int | None = None
    memory_util: int | None = None
    disk_util: int | None = None

    ssh_config_id: int | None = Field(default=None, foreign_key="sshconfig.id")
