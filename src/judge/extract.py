from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from spanrecorder.span import Span
from judge.rubrics.base import Rubric
from judge.prompts.templates import build_judge_prompt


@dataclass
class JudgeRequest:
    trace_id: str
    rubric_name: str
    prompt: str
    payload: Dict[str, Any]


def _first_attr(spans: List[Span], key: str) -> Optional[Any]:
    for s in spans:
        if key in (s.attributes or {}):
            return s.attributes[key]
    return None


def _kind_like(span: Span) -> str:
    attrs: Dict[str, Any] = span.attributes or {}
    return str(attrs.get("kind") or span.name or "").lower()


def build_judge_request(spans: Iterable[Span], rubric: Rubric) -> JudgeRequest:
    spans_list = list(spans)
    if not spans_list:
        raise ValueError("No spans")

    trace_id = spans_list[0].trace_id

    user_query = _first_attr(spans_list, "user.query") or _first_attr(spans_list, "request.query")
    final_answer = _first_attr(spans_list, "assistant.answer") or _first_attr(spans_list, "response.text")

    retrieved = []
    for s in spans_list:
        if _kind_like(s).startswith("retrieval"):
            passages = s.attributes.get("retrieval.passages") or s.attributes.get("passages")
            if passages:
                retrieved.append(passages)

    tools = []
    for s in spans_list:
        if _kind_like(s).startswith("tool"):
            tools.append(
                {
                    "name": s.attributes.get("tool.name") or s.attributes.get("name"),
                    "input": s.attributes.get("tool.input"),
                    "output": s.attributes.get("tool.output"),
                }
            )

    payload: Dict[str, Any] = {
        "user_query": user_query,
        "final_answer": final_answer,
        "retrieved_context": retrieved,
        "tool_calls": tools,
        "trace_metadata": {"trace_id": trace_id},
    }
    prompt = build_judge_prompt(payload, rubric)
    return JudgeRequest(trace_id=trace_id, rubric_name=rubric.name, prompt=prompt, payload=payload)
