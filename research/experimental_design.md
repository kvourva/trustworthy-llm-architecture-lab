# Experimental design

All experiments are reproducible scaffolds. The default seed is 42; repeat
with predeclared seeds and publish each output before making comparative
claims. No output is provided as a result. Synthetic data do not support
operational generalisation.

| ID | Comparison and unit | Measures | Main caveat |
|---|---|---|---|
| E1 | TF-IDF + LinearSVC vs. Dummy/LogisticRegression; optional fine-tuned small transformer on same stratified split | Accuracy, macro precision/recall/F1, per-class precision/recall, confusion matrix, high-risk false negatives, train/inference time | Include repeated seeds, model/version, hardware, memory; transformer is not run by default |
| E2 | TF-IDF lexical vs. optional dense Sentence Transformer on identical labelled queries/evidence | Precision@k, Recall@k, MRR, Hit Rate@k, latency | The built-in fixtures are illustrative; current runner does not claim dense metrics unless the optional adapter is enabled |
| E3 | Mock LLM alone vs. mock provider with RAG | Claim support, valid provenance, insufficient-evidence and failure rates | Mock behavior tests the pipeline contract only, not a real LLM |
| E4 | RAG with vs. without verification | Unsupported claims, verifier outcomes, end-to-end latency | Token-overlap verifier is a weak predictive baseline |
| E5 | Full recommendation routing vs. risk-tiered policy | Recommendation automation rate, escalation rate, high-risk false negatives, assumed approval latency | Current scaffold uses known generated labels; sensitivity to classifier errors is a future extension |
| E6 | Synthetic PII filter enabled vs. disabled | Precision, recall, false positives, leakage rate; downstream utility in a larger study | Tiny examples are a smoke test, not a performance estimate |

Run with `trustworthy-llm-experiment --experiment E1 ... E6 --seed 42`.
Outputs may be written to `results/`; generated records are not committed by
default. Optional model downloads require explicit `--include-optional` and
may be costly. Fix the split and parameters before comparing; tune only on
training/validation data. Report uncertainty across seeds and avoid
significance claims without a justified sampling model.
