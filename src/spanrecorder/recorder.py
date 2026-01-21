from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import contextvars
import uuid

from .span import Span, SpanStatus


_current_span_var: contextvars.ContextVar[Optional[Span]] = contextvars.ContextVar(
    "evaltrace_current_span",
    default=None,
)


def new_trace_id() -> str:
    return uuid.uuid4().hex


@dataclass
class SpanHandle:
    """Context manager returned by SpanRecorder.start_span(...).

    Usage:
        with recorder.start_span("retrieval", attrs={"top_k": 10}) as span:
            ...
    """

    recorder: "SpanRecorder"
    span: Span
    _token: Optional[contextvars.Token] = None

    def __enter__(self) -> Span:
        self._token = _current_span_var.set(self.span)
        self.recorder._on_span_start(self.span)
        return self.span

    def __exit__(self, exc_type, exc, tb) -> bool:
        if exc is not None:
            self.span.record_exception(exc)
            self.span.end(status=SpanStatus.ERROR)
        else:
            self.span.end(status=SpanStatus.OK)

        self.recorder._on_span_end(self.span)

        # Restore previous context (parent span)
        if self._token is not None:
            _current_span_var.reset(self._token)

        # Do not suppress exceptions
        return False


class SpanRecorder:
    """Minimal in-memory recorder for EvalTrace.

    Core API:
      - start_span(name, attrs=None, trace_id=None) -> context manager
      - current_span() -> Span | None
      - get_spans() -> List[Span]
      - to_dicts() -> List[dict]
      - reset() clears stored spans
    """

    def __init__(self) -> None:
        self._spans: List[Span] = []

    def reset(self) -> None:
        self._spans.clear()

    def current_span(self) -> Optional[Span]:
        return _current_span_var.get()

    def start_span(
        self,
        name: str,
        *,
        attrs: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ) -> SpanHandle:
        parent = self.current_span()

        resolved_trace_id = (
            trace_id
            if trace_id is not None
            else (parent.trace_id if parent is not None else new_trace_id())
        )

        span = Span(
            name=name,
            trace_id=resolved_trace_id,
            parent_id=parent.span_id if parent is not None else None,
        )

        if attrs:
            for k, v in attrs.items():
                span.set_attribute(k, v)

        return SpanHandle(recorder=self, span=span)

    def _on_span_start(self, span: Span) -> None:
        # Store immediately so spans appear even if the program crashes mid-span.
        self._spans.append(span)

    def _on_span_end(self, span: Span) -> None:
        # Hook for future: export-on-end, processors, sampling, etc.
        pass

    def get_spans(self) -> List[Span]:
        return list(self._spans)

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self._spans]
