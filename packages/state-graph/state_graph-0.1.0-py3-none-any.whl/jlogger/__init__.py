from .client import JLogger
from .server import run_server
import os
import threading
import requests
import time
from typing import Any
from beartype.claw import beartype_this_package
import atexit

beartype_this_package()

jlogger: JLogger | None = None
data_dir: str | None = None
server_thread: threading.Thread | None = None


def init(port: int, host: str = "localhost", data_directory: str = "data"):
    global jlogger, data_dir, server_thread
    assert os.path.exists(
        data_directory
    ), f"Data directory {data_directory} does not exist"
    base_url = f"http://{host}:{port}"
    data_dir = data_directory
    if jlogger is None:
        jlogger = JLogger(base_url)
        if server_thread is None or not server_thread.is_alive():
            server_thread = threading.Thread(
                target=run_server, args=(port, data_dir), daemon=True
            )
            server_thread.start()
        atexit.register(close)

    assert server_thread is not None, "Server thread is None"

    time.sleep(1)  # You might need to adjust this delay

    # Check if the server thread is alive
    if not server_thread.is_alive():
        raise RuntimeError("Failed to start the server thread.")

    # Check if the server is listening on the correct port
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # This will raise an error for 4xx/5xx responses
        # Optionally check the response content if your server returns a specific message
        # if response.text != "Expected response":
        #     raise RuntimeError("Server is up but returned an unexpected response.")
    except requests.RequestException as e:
        raise RuntimeError(f"Server is not responding as expected: {e}")


def log(id: str, data: dict[str, Any]) -> None:
    if jlogger is None:
        raise RuntimeError("jlogger is not initialized. Call init() first.")
    jlogger.log(id, data)


def close():
    global jlogger, server_thread
    if jlogger is not None:
        jlogger.close()
    if server_thread is not None:
        server_thread.join()
        server_thread = None
