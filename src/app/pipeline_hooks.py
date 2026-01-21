from __future__ import annotations

from spanrecorder.recorder import SpanRecorder


def instrumented_rag_example(rec: SpanRecorder, query: str) -> str:
    with rec.span("request", kind="request", attributes={"user.query": query, "component": "app"}):
        with rec.span("retrieval.search", kind="retrieval.search", attributes={"retrieval.top_k": 3}):
            passages = [
                {"id": "doc1", "text": "Example passage one."},
                {"id": "doc2", "text": "Example passage two."},
            ]
        rec.add_event_span("retrieval.result", kind="retrieval.result", attributes={"retrieval.passages": passages})

        with rec.span("llm.call", kind="llm.call", attributes={"component": "llm", "phase": "prefill"}):
            pass
        with rec.span("llm.call", kind="llm.call", attributes={"component": "llm", "phase": "decode"}):
            answer = "This is a placeholder answer."

        rec.add_event_span("response", kind="response", attributes={"assistant.answer": answer})
        return answer
