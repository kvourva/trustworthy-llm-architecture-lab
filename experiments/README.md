# Experiment runner

Run `trustworthy-llm-experiment --experiment E1 --seed 42` (E1–E6 supported),
or `python -m trustworthy_llm.experiments --experiment E5`. Add `--output
results/name.json` to save generated output. Seeds are explicit. These
scaffolds do not create or imply empirical findings.

E1 compares classical baselines and reports the optional transformer as not
run unless enabled. E2 currently runs the lexical arm; the dense adapter
requires external model packages and weights and must be run and measured
separately. E3/E4 use deterministic mock responses and are integration checks.
E5 uses synthetic known labels, not classifier predictions. E6 is a two-case
synthetic smoke experiment. See `research/experimental_design.md` for design
and interpretation constraints.
