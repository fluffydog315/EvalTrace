from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Protocol


class ResultStore(Protocol):
    def write(self, trace_id: str, kind: str, payload: Dict[str, Any]) -> None: ...
    def read(self, trace_id: str, kind: str) -> Dict[str, Any]: ...


@dataclass
class JsonResultStore:
    directory: str

    def _path(self, trace_id: str, kind: str) -> str:
        return os.path.join(self.directory, f"{trace_id}.{kind}.json")

    def write(self, trace_id: str, kind: str, payload: Dict[str, Any]) -> None:
        os.makedirs(self.directory, exist_ok=True)
        with open(self._path(trace_id, kind), "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def read(self, trace_id: str, kind: str) -> Dict[str, Any]:
        path = self._path(trace_id, kind)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
