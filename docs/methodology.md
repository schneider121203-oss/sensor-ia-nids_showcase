# Evaluation methodology

## Learning protocol

The system follows **unsupervised novelty detection with benign-only fitting**.
No attack label is required to fit EIF, the reconstruction Autoencoder, LOF,
the preprocessing artifacts, or the empirical score references.

The native benign flow collection was ordered chronologically and split
70/15/15:

| Partition | Flows | Purpose |
|---|---:|---|
| Training | 2,520 | Fit preprocessing, detectors, and score references |
| Validation | 540 | Calibrate the operating threshold against a predefined benign FPR target |
| Internal benign test | 540 | Estimate benign generalization after calibration |

The three normalized anomaly percentiles are combined using equal weights.
Higher scores consistently mean greater anomaly.

## Controlled evaluation

Evaluation was performed in an isolated AWS laboratory using owned systems and
bounded commands. The locked evaluation cohort contains:

| Ground-truth class | Flows |
|---|---:|
| Attack-associated | 908 |
| Benign | 544 |
| Total | 1,452 |

The resulting confusion matrix is `TP=867`, `FP=25`, `TN=519`, `FN=41`.
The published metrics are derived directly from these four counts.

## Interpretation constraints

- Labels describe the execution in which a flow was observed; they are not
  per-flow forensic adjudications.
- Flows within one run are correlated observations.
- Only one valid repetition was available for each offensive scenario.
- The experiment measures controlled AWS behavior, not production performance.
- Packet captures, flow datasets, and trained artifacts are withheld for
  privacy, security, and repository-size reasons.

Accordingly, this repository supports arithmetic verification and architectural
review, but not complete reproduction of model training or packet-level replay.
