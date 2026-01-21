import asyncio
import pytest

from spanrecorder import SpanRecorder, SpanStatus


def test_single_span_records_and_ends():
    r = SpanRecorder()
    with r.start_span("rag.request", attrs={"user": "olivia"}) as sp:
        assert sp.name == "rag.request"
        assert sp.attributes["user"] == "olivia"
        assert sp.end_ns is None

    spans = r.get_spans()
    assert len(spans) == 1
    s = spans[0]
    assert s.end_ns is not None
    assert s.duration_ns is not None and s.duration_ns >= 0
    assert s.status == SpanStatus.OK


def test_nested_spans_parent_child_relationship():
    r = SpanRecorder()
    with r.start_span("root") as root:
        with r.start_span("child") as child:
            pass

    spans = r.get_spans()
    assert len(spans) == 2

    root_span = spans[0]
    child_span = spans[1]

    assert root_span.parent_id is None
    assert child_span.parent_id == root_span.span_id
    assert child_span.trace_id == root_span.trace_id


def test_exception_marks_error_and_records_exception_fields():
    r = SpanRecorder()
    with pytest.raises(ValueError):
        with r.start_span("tool.call") as sp:
            sp.add_event("starting")
            raise ValueError("boom")

    s = r.get_spans()[0]
    assert s.status == SpanStatus.ERROR
    assert s.exception_type == "ValueError"
    assert s.exception_message == "boom"
    assert s.end_ns is not None


def test_current_span_tracks_active_span():
    r = SpanRecorder()
    assert r.current_span() is None

    with r.start_span("a") as a:
        assert r.current_span() is a
        with r.start_span("b") as b:
            assert r.current_span() is b
        assert r.current_span() is a

    assert r.current_span() is None


@pytest.mark.asyncio
async def test_async_context_propagation_with_contextvars():
    r = SpanRecorder()
    results = {}

    async def child_task():
        cur = r.current_span()
        results["cur_name"] = None if cur is None else cur.name

    with r.start_span("async.root"):
        await asyncio.create_task(child_task())

    assert results["cur_name"] == "async.root"
