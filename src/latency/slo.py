from __future__ import annotations

from dataclasses import dataclass

from .aggregate import LatencyReport


@dataclass(frozen=True, slots=True)
class LatencySLO:
    name: str
    p95_ms_max: float


@dataclass(frozen=True, slots=True)
class SLOResult:
    slo_name: str
    passed: bool
    observed_p95_ms: float
    budget_ms: float


def evaluate_latency_slo(report: LatencyReport, slo: LatencySLO) -> SLOResult:
    return SLOResult(
        slo_name=slo.name,
        passed=report.p95_ms <= slo.p95_ms_max,
        observed_p95_ms=report.p95_ms,
        budget_ms=slo.p95_ms_max,
    )
