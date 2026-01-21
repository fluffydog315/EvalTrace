"""EvalTrace SpanRecorder (minimal core).

This package provides:
  - Span / Event model
  - Async-safe context propagation via contextvars
  - In-memory SpanRecorder with a context-manager API
"""

from .span import Span, SpanEvent, SpanStatus
from .recorder import SpanRecorder, new_trace_id

__all__ = ["Span", "SpanEvent", "SpanStatus", "SpanRecorder", "new_trace_id"]
