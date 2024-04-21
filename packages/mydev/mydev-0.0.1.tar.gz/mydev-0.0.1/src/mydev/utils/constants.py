import os

MYDEV_DIR = os.path.abspath(os.path.join(os.path.expanduser("~"), ".mydev"))

MYDEV_PM_DIR = os.path.join(MYDEV_DIR, "pm")
MYDEV_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

MYDEV_DB_PATH = os.path.join(MYDEV_DIR, "db.sqlite")
MYDEV_DB_URL = f"sqlite:///{MYDEV_DB_PATH}"

MYDEV_CONFIG_PATH = os.path.join(MYDEV_DIR, "config.json")

os.makedirs(MYDEV_DIR, exist_ok=True)
os.makedirs(MYDEV_PM_DIR, exist_ok=True)
