# EvalTrace

**Span-level observability and evaluation for RAG and LLM applications**

EvalTrace helps AI engineers understand why their AI systems change —  
not just that they changed.

> Detect latency regressions, cost anomalies, and quality drops using structured tracing and AI-as-Judge evaluation.



## 🚨 The Problem

Modern LLM systems fail silently:

- Latency spikes hide inside retrieval, tool calls, or decoding
- Prompt or model changes cause subtle hallucinations
- Regressions ship without clear correctness signals

Traditional observability shows *infrastructure health*,  
but not *AI behavior*.



## ✨ What EvalTrace Does

EvalTrace decomposes every AI request into **observable spans** and evaluates output quality using **AI-as-Judge**.

**You can answer questions like:**
- Why did p95 latency increase?
- Which phase regressed — retrieval or decoding?
- Did quality drop after a prompt change?
- Are faster responses less accurate?



## 🔍 Key Features

- **Span-level latency breakdown**
  - Retrieval → Tool calls → LLM prefill → LLM decode → Post-processing
- **AI-as-Judge quality scoring**
  - Correctness, faithfulness, completeness, clarity
- **Regression detection**
  - Compare latency and quality across runs or deployments
- **Vendor-agnostic instrumentation**
  - Works with any RAG or LLM stack



## 🧠 Architecture Overview

```text
EvalTrace/
├── spanrecorder/
│   ├── Span / Event model
│   ├── Async-safe context propagation
│   └── Pluggable exporters
│
├── latency/
│   ├── Phase-level breakdown
│   └── Regression analysis
│
├── judge/
│   ├── Structured rubric
│   ├── JSON scoring
│   └── Confidence tracking
│
└── dashboard/
    ├── Trace view
    ├── Latency charts
    └── Quality trends
```



## 🚀 Quickstart

```python
from evaltrace import recorder

with recorder.start_span("rag.request"):
    with recorder.start_span("retrieval", attrs={"top_k": 8}):
        docs = retrieve(query)

    with recorder.start_span("llm.decode"):
        answer = generate(query, docs)
```

Get structured traces and metrics **without coupling to a vendor SDK**.



## 📊 Dashboards (Preview)

**Latency Breakdown**
- Waterfall view by span type
- p50 / p95 trends over time

**Quality Trends**
- AI-as-Judge scores per deployment
- Correlation with latency and cost

> Screenshots coming soon



## 🤖 AI-as-Judge (Clear Rubric)

Each response is scored using a fixed rubric:

| Dimension     | Scale |
|--------------|-------|
| Correctness  | 1–5   |
| Faithfulness | 1–5   |
| Completeness | 1–5   |
| Clarity      | 1–5   |

Judges return **strict JSON**, enabling aggregation and regression analysis.



## 🎯 Who This Is For

EvalTrace is built for:

- AI Engineers
- ML Platform Engineers
- Tech Leads shipping LLM products

If you care about **why your AI system changed**, EvalTrace is for you.



## 🛣 Roadmap

- [ ] OpenTelemetry exporter
- [ ] Persistent span storage
- [ ] Automated quality regression alerts
- [ ] Human + AI hybrid evaluation
- [ ] Production-grade dashboard



## 📚 Learn More

- Full design and metrics: `docs/architecture.md`
- AI-as-Judge details: `docs/judge.md`



## Why EvalTrace

EvalTrace bridges the gap between **observability** and **evaluation**.

It doesn’t just tell you *something went wrong* —  
it tells you **where**, **why**, and **whether it matters**.
