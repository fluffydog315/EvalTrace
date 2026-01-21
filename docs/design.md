# EvalTrace

**EvalTrace** is a span-level observability and evaluation framework for RAG and LLM applications, designed to surface **latency regressions, cost anomalies, and quality failures** using both traditional metrics and **AI-as-Judge evaluation**.

EvalTrace answers a simple question:

> *Is my AI system getting slower, more expensive, or less correct — and why?*

---

## Motivation

Modern AI applications (RAG, agents, tool-using LLMs) fail in non-obvious ways:

- Latency spikes inside retrieval, tool calls, or decoding
- Silent quality regressions after prompt or model changes
- No clear linkage between latency, cost, and correctness

EvalTrace provides **structured observability + evaluation**, not just logs.

---

## Problem → Design → Implementation → Metrics → Limitations

---

## 1. Problem

Traditional observability focuses on infrastructure metrics and request-level latency.

AI systems fail *inside* a request:
- Retrieval vs tool calls vs LLM prefill vs decode
- Hallucinations caused by prompt or retrieval drift
- Regressions that are invisible without structured evaluation

---

## 2. Design

EvalTrace follows three principles:

### Span-first observability
Every AI request is decomposed into structured spans with timing, attributes, and hierarchy.

### Evaluation as a first-class signal
Model quality is treated as measurable data, not anecdotal feedback.

### Decoupled instrumentation
Application code is vendor-agnostic; exporters and dashboards evolve independently.

---

## 3. Implementation

### Architecture Overview

```text
EvalTrace/
├── spanrecorder/
│   ├── Span / Event model
│   ├── Context propagation (async-safe)
│   └── In-memory + pluggable exporters
│
├── latency/
│   ├── Breakdown by phase
│   └── Regression detection
│
├── judge/
│   ├── Prompted rubric
│   ├── Structured scoring
│   └── Confidence tracking
│
└── dashboard/
    ├── Trace view
    ├── Latency charts
    └── Quality trends
```

---

## 4. Metrics

EvalTrace tracks three orthogonal metric families.

### 4.1 Latency Metrics

- Retrieval latency
- Tool call latency
- LLM prefill latency
- LLM decode latency
- Post-processing latency

**Screenshot (placeholder):**
Latency breakdown waterfall by span type.

---

### 4.2 Cost Metrics

- Token usage per span
- Cost attribution per request
- Prompt vs decode cost split

---

## 4.3 Quality Metrics (AI-as-Judge)

EvalTrace treats **output quality as an observable metric**, not an offline annotation task.

### Evaluation Approach

- Reference-based evaluation
- Preference-based evaluation
- Model-as-Judge evaluation (initial focus)

---

### Judge Rubric

| Dimension     | Description                                   | Scale |
|--------------|-----------------------------------------------|-------|
| Correctness  | Factual accuracy vs retrieved context         | 1–5   |
| Faithfulness | Avoids hallucination                          | 1–5   |
| Completeness | Fully answers the user question               | 1–5   |
| Clarity      | Clear and well-structured response            | 1–5   |

---

### Judge Prompt (Example)

```text
You are an AI evaluator.

User Question:
{user_query}

Retrieved Context:
{retrieved_documents}

Model Answer:
{model_answer}

Evaluate the answer using the following rubric:
1. Correctness (1–5)
2. Faithfulness (1–5)
3. Completeness (1–5)
4. Clarity (1–5)

Return valid JSON only. No explanations.
```

---

### Example Judge Output

```json
{
  "correctness": 4,
  "faithfulness": 5,
  "completeness": 4,
  "clarity": 5
}
```

---

### Quality Tracking

EvalTrace enables:
- Quality score trends
- Regression detection
- Correlation between latency, cost, and quality

---

## 5. Limitations

- AI-as-Judge is probabilistic, not ground truth
- Judge models may introduce bias or variance
- LLM internal latency is partially observable
- Default recorder is in-memory only

---

## Roadmap

- [ ] Persistent span storage
- [ ] OpenTelemetry exporter
- [ ] Automated regression detection
- [ ] Human-in-the-loop evaluation
- [ ] Alerting on quality degradation

---

## Why EvalTrace

EvalTrace is designed for engineers shipping real AI systems.

If you care about:
- Why your AI system changed
- Catching regressions early
- Measuring quality, not just speed

EvalTrace provides the missing observability layer.
