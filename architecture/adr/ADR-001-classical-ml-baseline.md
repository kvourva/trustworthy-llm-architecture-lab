# ADR-001: Classical TF-IDF risk baseline

- **Status:** Accepted for research baseline
- **Context:** A transparent reference is needed before adding higher-complexity models.
- **Decision:** Use TF-IDF word unigrams/bigrams with DummyClassifier, class-weighted LogisticRegression, and LinearSVC. Normalize case and whitespace for this classical pipeline only.
- **Alternatives:** Keyword rules, RandomForest, transformer-only classifier, no baseline.
- **Rationale:** Sparse linear models are reproducible, inexpensive, and their feature weights can be inspected. Dummy performance anchors the comparison.
- **Positive consequences:** Offline, fast, interpretable feature space; macro and per-class error analysis is feasible.
- **Negative consequences:** Bag-of-words misses context and paraphrase; synthetic lexical templates can inflate scores.
- **Trustworthiness implications:** Reliability is assessed by per-class recall and severe false negatives; inspectability is not proof of faithful explanation.
- **Evaluation plan:** Fixed stratified split and seeds; accuracy, macro precision/recall/F1, class metrics, confusion matrix, latency, HIGH/CRITICAL misses.
