import os

from fastapi import FastAPI
from fastapi.responses import FileResponse

from mydev.utils.constants import MYDEV_ASSETS_DIR

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.get("/install.sh")
async def serve_install_script():
    return FileResponse(os.path.join(MYDEV_ASSETS_DIR, "install.sh"))


@app.post("/agent")
async def agent():
    return {"Hello": "World"}
