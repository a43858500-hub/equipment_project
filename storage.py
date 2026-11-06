import json
from pathlib import Path

from models import Equipment

def load_equipment(path) -> list[Equipment]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Equipment(**item) for item in data]
