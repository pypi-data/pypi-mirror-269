from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/agent")
async def agent():
    return {"Hello": "World"}
