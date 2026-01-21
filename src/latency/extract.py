from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from spanrecorder.span import Span
from .taxonomy import classify


@dataclass
class LatencyFeatures:
    trace_id: str
    total_ms: float
    by_component_ms: Dict[str, float] = field(default_factory=dict)
    by_component_phase_ms: Dict[Tuple[str, str], float] = field(default_factory=dict)
    root_span_id: Optional[str] = None
    span_count: int = 0

    def to_dict(self) -> Dict:
        return {
            "trace_id": self.trace_id,
            "total_ms": self.total_ms,
            "by_component_ms": dict(self.by_component_ms),
            "by_component_phase_ms": {f"{k[0]}:{k[1]}": v for k, v in self.by_component_phase_ms.items()},
            "root_span_id": self.root_span_id,
            "span_count": self.span_count,
        }


def _find_root(spans: List[Span]) -> Optional[Span]:
    roots = [s for s in spans if s.parent_id is None]
    if not roots:
        return None
    return sorted(roots, key=lambda s: s.start_ns)[0]


def _duration_ms(span: Span) -> float:
    """Convert your Span.duration_ns (Optional[int]) to ms."""
    dn = span.duration_ns
    if dn is None:
        return 0.0
    return float(dn) / 1_000_000.0


def extract_latency(spans: Iterable[Span]) -> LatencyFeatures:
    spans_list = list(spans)
    if not spans_list:
        raise ValueError("No spans")

    trace_id = spans_list[0].trace_id
    root = _find_root(spans_list)
    total_ms = _duration_ms(root) if root else max(_duration_ms(s) for s in spans_list)

    by_comp: Dict[str, float] = {}
    by_comp_phase: Dict[Tuple[str, str], float] = {}

    for s in spans_list:
        ms = _duration_ms(s)
        p = classify(s)
        by_comp[p.component] = by_comp.get(p.component, 0.0) + ms
        if p.phase:
            key = (p.component, p.phase)
            by_comp_phase[key] = by_comp_phase.get(key, 0.0) + ms

    return LatencyFeatures(
        trace_id=trace_id,
        total_ms=total_ms,
        by_component_ms=by_comp,
        by_component_phase_ms=by_comp_phase,
        root_span_id=root.span_id if root else None,
        span_count=len(spans_list),
    )
