import json, os, time, uuid
from typing import Any, Dict

class JSONLLogger:
    def __init__(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path

    def log(self, record: Dict[str, Any]) -> str:
        rec = dict(record)
        rec.setdefault("timestamp", time.time())
        rec.setdefault("run_id", str(uuid.uuid4()))
        line = json.dumps(rec, ensure_ascii=False)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        return rec["run_id"]
