from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterable, List, Protocol

from spanrecorder.span import Span


class TraceStore(Protocol):
    def write(self, spans: Iterable[Span]) -> None: ...
    def read_all(self) -> List[Span]: ...


@dataclass
class JsonlTraceStore:
    path: str

    def write(self, spans: Iterable[Span]) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as f:
            for s in spans:
                f.write(json.dumps(s.to_dict(), ensure_ascii=False) + "\n")

    def read_all(self) -> List[Span]:
        if not os.path.exists(self.path):
            return []
        spans: List[Span] = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                spans.append(Span.from_dict(json.loads(line)))
        return spans
