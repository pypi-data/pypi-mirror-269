from pyairtable import Base
import requests
import json
import ipdb
from typing import Any
from rich import print
from pydantic import BaseModel


def base_models_to_dict(
    data: BaseModel | dict[str, Any] | list[Any]
) -> dict[str, Any] | list[Any] | Any:
    if isinstance(data, BaseModel):
        return data.model_dump()
    elif isinstance(data, dict):
        return {k: base_models_to_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [base_models_to_dict(item) for item in data]
    else:
        return data


class JLogger:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

    def log(self, id: str, data: dict[str, Any] | BaseModel) -> None:
        data_cleaned = base_models_to_dict(data)
        try:
            json_data = json.dumps(data_cleaned)
        except json.JSONDecodeError as e:
            print(data_cleaned)
            raise e
        assert isinstance(json_data, str)
        payload = {"id": id, "json_value": json_data}
        post_url = f"{self.base_url}/update"
        print(f"{post_url=}")
        response = self.session.post(post_url, json=payload)
        response.raise_for_status()

    def close(self):
        try:
            response = self.session.post(f"{self.base_url}/shutdown")
            response.raise_for_status()
        except requests.exceptions.RequestException:
            pass
        self.session.close()
