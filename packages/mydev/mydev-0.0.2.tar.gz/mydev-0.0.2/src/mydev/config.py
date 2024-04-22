import os
from typing import Optional

from pydantic import BaseModel

from mydev.utils.constants import MYDEV_CONFIG_PATH


class Config(BaseModel):
    username: Optional[str] = None
    local_user_id: Optional[int] = None


def try_load_config(config_path: str = MYDEV_CONFIG_PATH) -> Config:
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            cfg = Config.model_validate_json(f.read())
    else:
        cfg = Config()
    return cfg


def save_config(cfg: Config, config_path: str = MYDEV_CONFIG_PATH):
    with open(config_path, "w") as f:
        f.write(cfg.model_dump_json())
