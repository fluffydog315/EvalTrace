import json

from spanrecorder.span import Span
from spanrecorder.recorder import SpanRecorder
from judge.extract import build_judge_request
from judge.rubrics.rag_answer_quality import RagAnswerQualityRubric
from judge.runner import run_judge


class FakeJudgeClient:
    def complete(self, prompt: str) -> str:
        return json.dumps({"scores": {"correctness": 4, "grounding": 5}, "overall": 4, "rationale": "ok"})


def test_build_and_run_judge():
    rec = SpanRecorder()
    with rec.start_span("request", attrs={"kind": "request", "user.query": "q"}):
        # store answer as a child span so it has a duration and is recorded consistently
        with rec.start_span("response", attrs={"kind": "response", "assistant.answer": "a"}):
            pass

    spans = rec.get_spans()

    rubric = RagAnswerQualityRubric()
    req = build_judge_request(spans, rubric)
    assert req.trace_id
    assert "EVALUATION_INPUT" in req.prompt

    res = run_judge(req, FakeJudgeClient())
    assert res.scores["correctness"] == 4
    assert res.overall == 4
