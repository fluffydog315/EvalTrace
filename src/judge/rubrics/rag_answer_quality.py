from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .base import RubricScore


@dataclass(frozen=True, slots=True)
class RagAnswerQualityRubric:
    name: str = "rag_answer_quality"
    instructions: str = (
        "You are grading a RAG system answer. Score each dimension on the provided scale. "
        "Prefer evidence-based, grounded answers. Penalize hallucinations and unsupported claims."
    )
    dimensions: List[RubricScore] = (
        RubricScore("correctness", 1, 5, "Is the answer correct given the retrieved context?"),
        RubricScore("grounding", 1, 5, "Does the answer rely on retrieved context (no hallucinations)?"),
        RubricScore("completeness", 1, 5, "Does it fully address the user question?"),
        RubricScore("clarity", 1, 5, "Is it clear and easy to follow?"),
    )

    def as_dict(self) -> Dict:
        return {
            "name": self.name,
            "instructions": self.instructions,
            "dimensions": [
                {
                    "key": d.key,
                    "scale_min": d.scale_min,
                    "scale_max": d.scale_max,
                    "description": d.description,
                }
                for d in self.dimensions
            ],
        }
