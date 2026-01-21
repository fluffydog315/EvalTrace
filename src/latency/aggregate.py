from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

from .extract import LatencyFeatures


def _percentile(xs: List[float], p: float) -> float:
    if not xs:
        return 0.0
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    if f == c:
        return xs[f]
    return xs[f] + (xs[c] - xs[f]) * (k - f)


@dataclass
class LatencyReport:
    n: int
    p50_ms: float
    p95_ms: float
    p99_ms: float
    avg_ms: float
    component_avg_ms: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "n": self.n,
            "p50_ms": self.p50_ms,
            "p95_ms": self.p95_ms,
            "p99_ms": self.p99_ms,
            "avg_ms": self.avg_ms,
            "component_avg_ms": dict(self.component_avg_ms),
        }


def aggregate_latency(features: Iterable[LatencyFeatures]) -> LatencyReport:
    feats = list(features)
    if not feats:
        raise ValueError("No latency features")

    totals = [f.total_ms for f in feats]
    n = len(totals)
    avg = sum(totals) / n

    comp_sums: Dict[str, float] = {}
    for f in feats:
        for comp, ms in f.by_component_ms.items():
            comp_sums[comp] = comp_sums.get(comp, 0.0) + ms
    comp_avg = {k: v / n for k, v in comp_sums.items()}

    return LatencyReport(
        n=n,
        p50_ms=_percentile(totals, 0.50),
        p95_ms=_percentile(totals, 0.95),
        p99_ms=_percentile(totals, 0.99),
        avg_ms=avg,
        component_avg_ms=comp_avg,
    )
