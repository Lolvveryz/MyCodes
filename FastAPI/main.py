from typing import Union

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return


@app.get("/print/{item_id}")
def prints(item_id):
    return item_id


@app.get("/{first}/{second}")
def add(first: int, second: int):
    return first + second


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
