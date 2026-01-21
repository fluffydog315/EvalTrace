from __future__ import annotations

import json
from typing import Any, Dict, Protocol

from judge.extract import JudgeRequest
from judge.scoring import JudgeResult, normalize_judge_output


class JudgeClient(Protocol):
    def complete(self, prompt: str) -> str:
        ...


def run_judge(req: JudgeRequest, client: JudgeClient) -> JudgeResult:
    raw_text = client.complete(req.prompt)
    try:
        parsed: Dict[str, Any] = json.loads(raw_text)
    except Exception:
        parsed = {"scores": {}, "rationale": "Non-JSON output from judge model", "raw_text": raw_text}

    return normalize_judge_output(req.trace_id, req.rubric_name, parsed)
