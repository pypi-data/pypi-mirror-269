from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os

# import json
import json5
import uvicorn
import asyncio

app: FastAPI = FastAPI()
server: uvicorn.Server | None = None
data_dir: str | None = None


class UpdateRequest(BaseModel):
    id: str
    json_value: str


@app.post("/update")
async def update_jsonl(request: UpdateRequest):
    assert data_dir is not None
    id = request.id
    json_data = request.json_value
    assert os.path.exists(data_dir), f"Data directory {data_dir} does not exist"
    file_path = os.path.join(data_dir, f"{id}.json")

    try:
        data = json5.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {e}")

    old_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            old_data = json5.load(file)

    assert isinstance(old_data, list), "Old data is not a list"
    if isinstance(data, list):
        new_data = old_data + data
    else:
        new_data = old_data + [data]
    try:
        with open(file_path, "w") as file:
            json5.dump(new_data, file, indent=2)
        return {"message": "JSONL file updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.post("/shutdown")
async def shutdown():
    global server
    if server is not None:
        await server.shutdown()
        server = None


async def start_server(port: int):
    global server
    config = uvicorn.Config(app, host="localhost", port=port, log_level="warning")
    server = uvicorn.Server(config)
    await server.serve()


def run_server(port: int, data_directory: str):
    global data_dir
    data_dir = data_directory
    asyncio.run(start_server(port))
