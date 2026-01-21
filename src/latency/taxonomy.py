from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from spanrecorder.span import Span


@dataclass(frozen=True, slots=True)
class Phase:
    component: str            # retriever, tool, llm, postprocess, app
    phase: Optional[str] = None   # prefill, decode


def _kind_like(span: Span) -> str:
    """Return a lowercase kind-ish string.

    Your Span model doesn't have `kind`, so we use:
      1) attributes['kind'] if provided
      2) span.name otherwise
    """
    attrs: Dict[str, Any] = span.attributes or {}
    return str(attrs.get("kind") or span.name or "").lower()


def classify(span: Span) -> Phase:
    """Map spans into canonical latency buckets."""
    attrs: Dict[str, Any] = span.attributes or {}

    # Explicit override wins
    if "component" in attrs:
        return Phase(component=str(attrs["component"]), phase=attrs.get("phase"))

    kind = _kind_like(span)

    if kind.startswith("retrieval"):
        return Phase(component="retriever")
    if kind.startswith("tool"):
        return Phase(component="tool")
    if kind.startswith("llm"):
        phase = attrs.get("phase")
        if phase in ("prefill", "decode"):
            return Phase(component="llm", phase=str(phase))
        return Phase(component="llm")
    if kind.startswith("postprocess"):
        return Phase(component="postprocess")

    return Phase(component="app")
