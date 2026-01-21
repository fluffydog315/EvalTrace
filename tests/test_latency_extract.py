from spanrecorder.recorder import SpanRecorder
from latency.extract import extract_latency


def test_extract_latency_components():
    rec = SpanRecorder()
    with rec.start_span("request", attrs={"kind": "request"}):
        with rec.start_span("retrieval.search", attrs={"kind": "retrieval.search"}):
            pass
        with rec.start_span("tool.call", attrs={"kind": "tool.call"}):
            pass
        with rec.start_span("llm.call", attrs={"kind": "llm.call", "phase": "prefill"}):
            pass
        with rec.start_span("llm.call", attrs={"kind": "llm.call", "phase": "decode"}):
            pass

    feats = extract_latency(rec.get_spans())
    assert feats.total_ms >= 0
    assert "retriever" in feats.by_component_ms
    assert "tool" in feats.by_component_ms
    assert "llm" in feats.by_component_ms
    assert ("llm", "prefill") in feats.by_component_phase_ms
    assert ("llm", "decode") in feats.by_component_phase_ms
