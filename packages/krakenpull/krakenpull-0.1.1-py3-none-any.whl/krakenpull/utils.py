import json
import os
from pathlib import Path
from typing import Any


def get_root_dir():
    return Path(os.getenv("ROOT_DIRECTORY", Path(__file__).parents[1]))


def load_json(path: Path) -> Any:
    with open(get_root_dir() / path, "r") as f:
        return json.load(f)
