import json
from pathlib import Path

def read_json(file_name: str):
    project_root = Path(__file__).resolve().parents[1]
    file_path = project_root / "test_data" / file_name
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)