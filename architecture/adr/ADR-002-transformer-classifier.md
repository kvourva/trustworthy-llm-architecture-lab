# ADR-002: Optional transformer classifier

- **Status:** Accepted as an isolated optional experiment
- **Context:** RQ2 asks whether contextual representations justify added cost over TF-IDF.
- **Decision:** Provide an opt-in Hugging Face fine-tuning adapter for a small sequence model. Model files are local by default; downloads require explicit opt-in; remote custom model code is disabled.
- **Alternatives:** TF-IDF only, zero-shot LLM classification, larger encoder, no transformer comparison.
- **Rationale:** A controlled comparison can examine paraphrase sensitivity and cost without imposing downloads on core installation.
- **Positive consequences:** Same four labels and text task can be compared; model boundary is replaceable.
- **Negative consequences:** Training, memory, versioning, model supply-chain, and latency costs; no result is meaningful without a defensible split and repeated runs.
- **Trustworthiness implications:** Better contextual representation is not equivalent to calibrated confidence or explainability. External model packages/weights are outside core tests.
- **Evaluation plan:** Same seeded split as classical baseline; metrics, training/inference time, peak memory and parameter count. Report optional execution or explicitly mark not run.
