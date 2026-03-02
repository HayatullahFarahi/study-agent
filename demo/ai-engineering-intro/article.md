# AI Engineering Fundamentals — A Demo Article

> This is a short demo article included with study-agent so you can try the system immediately after cloning. It covers core concepts every AI engineer needs to know.

---

## 1. The AI Engineering Stack

AI engineering sits at the intersection of machine learning, software engineering, and product thinking. Unlike ML research, which focuses on pushing model accuracy, AI engineering focuses on building **reliable, production-grade systems** around AI models.

The modern AI engineering stack has three layers:

```
┌─────────────────────────────────┐
│       Application Layer         │  ← UI, APIs, orchestration
├─────────────────────────────────┤
│       Model Layer               │  ← Foundation models, fine-tuned models
├─────────────────────────────────┤
│       Data & Infra Layer        │  ← Vector DBs, pipelines, evaluation
└─────────────────────────────────┘
```

The key insight: most value in AI engineering comes from the **application and data layers**, not the model itself. The model is a commodity — what you build around it is the competitive advantage.

---

## 2. Foundation Models and Prompting

Foundation models (GPT-4, Claude, Gemini, Llama) are large language models pre-trained on massive datasets. Rather than training a model from scratch, AI engineers **adapt** these models through prompting and fine-tuning.

### Prompting strategies (in order of complexity)

| Strategy | Description | When to use |
|---|---|---|
| Zero-shot | Just ask the model directly | Simple tasks, well-defined outputs |
| Few-shot | Provide 2-5 examples before the question | When format or style matters |
| Chain-of-thought | Ask the model to reason step by step | Math, logic, multi-step problems |
| ReAct | Combine reasoning with tool calls | Agentic tasks, information retrieval |

A well-engineered prompt can close the gap between a mediocre and a great system — often more effectively than switching to a bigger model.

---

## 3. Retrieval-Augmented Generation (RAG)

RAG solves the biggest limitation of foundation models: they don't know your private data, and their training data has a cutoff date.

### How RAG works

1. **Chunk** your documents into small passages (200-500 tokens)
2. **Embed** each chunk into a vector using an embedding model
3. **Store** vectors in a vector database (Pinecone, Weaviate, Chroma)
4. At query time, **retrieve** the top-k most similar chunks
5. **Inject** retrieved chunks into the prompt as context
6. The model **generates** an answer grounded in your actual data

```
User Query ──▶ Embed ──▶ Vector Search ──▶ Top-K Chunks
                                               │
                                               ▼
                              Prompt: "Given this context: {chunks}
                                       Answer: {query}"
                                               │
                                               ▼
                                         LLM Response
```

### Key trade-offs

- **Chunk size**: Too small = lost context. Too large = noise drowns the signal.
- **Top-k**: Too few = missing information. Too many = exceeds context window.
- **Embedding model**: Must match the domain. Generic embeddings underperform on specialized text (legal, medical).

---

## 4. Evaluation and Testing

The hardest part of AI engineering isn't building — it's knowing whether your system actually works. Traditional software has deterministic tests; AI systems produce probabilistic outputs.

### Three levels of AI evaluation

**Level 1 — Component evaluation**
Test individual pieces: Does the retriever return relevant chunks? Does the prompt produce the right format?

**Level 2 — End-to-end evaluation**
Test the full pipeline: Given a user question, is the final answer correct, complete, and grounded?

**Level 3 — Production monitoring**
Track real-world performance: latency, error rates, user feedback, hallucination detection.

### Evaluation metrics for RAG

| Metric | What it measures |
|---|---|
| **Faithfulness** | Is the answer supported by the retrieved context? |
| **Relevance** | Are the retrieved chunks actually relevant to the query? |
| **Correctness** | Is the final answer factually accurate? |
| **Completeness** | Does the answer cover all parts of the question? |

The golden rule: **if you can't evaluate it, you can't improve it.**

---

## 5. From Prototype to Production

The gap between a demo and a production AI system is enormous. Here's what changes:

| Aspect | Prototype | Production |
|---|---|---|
| Latency | Doesn't matter | < 2 seconds P95 |
| Cost | $0.10/query is fine | Must optimize to $0.001/query |
| Reliability | "Works on my laptop" | 99.9% uptime, graceful degradation |
| Safety | Trust the model | Guardrails, content filters, human-in-the-loop |
| Evaluation | "Looks good to me" | Automated eval suites, A/B testing |

### Production checklist

- [ ] Rate limiting and cost controls
- [ ] Caching frequent queries
- [ ] Fallback behavior when the model fails
- [ ] Logging all inputs/outputs for debugging
- [ ] Guardrails for harmful or off-topic outputs
- [ ] Latency monitoring and alerting

---

## Summary

| Concept | Core Idea |
|---|---|
| AI Engineering Stack | Value comes from application + data layers, not just the model |
| Foundation Models | Adapt via prompting — zero-shot, few-shot, chain-of-thought, ReAct |
| RAG | Ground model answers in your private data via retrieval |
| Evaluation | Three levels: component, end-to-end, production monitoring |
| Prototype → Production | Bridge the gap with caching, guardrails, eval suites, and monitoring |

These five concepts form the foundation of modern AI engineering.
