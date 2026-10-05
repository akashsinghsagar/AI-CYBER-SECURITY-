# AI-Driven Cyber Threat Awareness and Detection Prototype

Mini project for **ENSP355: AI in Cyber Security Lab**. This repository
implements an end-to-end, educational intrusion-detection workflow using the
NSL-KDD-style network connection data already supplied with the project.

## What is included

* **Task 1 - Bootstrap:** reproducible `requirements.txt`, `.gitignore`,
  `data/`, `src/`, and a Python virtual-environment workflow.
* **Task 2 - EDA:** class-balance, suspicious-indicator, and
  attack-feature-distribution plots.
* **Task 3 - Classical ML:** leakage-safe imputation, one-hot encoding,
  standardisation, Logistic Regression, and accuracy/precision/recall/F1.
* **Task 4 - Deep-learning prototype:** an `MLPClassifier` neural network,
  compared with Logistic Regression on the same split and features, including
  training time.

## Project layout

```text
data/                           Dataset documentation and optional CSV copies
src/analysis_pipeline.py        Reproducible EDA + ML + MLP pipeline
Network_intrusion_detection.ipynb  Original exploratory notebook
Train_data.csv                  Labeled training data
Test_data.csv                   Unlabeled evaluation/prediction data
outputs/                        Generated plots, metrics, and predictions
```

## Run on Windows

```powershell
py -3.10 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\src\analysis_pipeline.py
```

If PowerShell blocks activation, call the interpreter directly:

```powershell
.\venv\Scripts\python.exe .\src\analysis_pipeline.py
```

The command creates `outputs/` containing:

* `class_distribution.png`
* `feature_distributions.png`
* `threat_indicators.png`
* `model_metrics.csv`
* `detailed_metrics.json`
* predictions for both models on `Test_data.csv`

`Test_data.csv` has no target labels, so its predictions are not used for
scoring. The metrics are calculated on a stratified validation split of the
labeled training data. This makes the comparison fair and avoids pretending
that unlabeled data has known outcomes.

## Interpretation and practical feasibility

Logistic Regression is a fast, transparent baseline. The MLP is a small neural
network prototype and may capture non-linear relationships, but it requires
more training time and careful monitoring. Accuracy alone is not sufficient
for an operational IDS: recall matters for missed attacks, while precision
matters for analyst workload and false alarms. Thresholds should be tuned on
representative production data before deployment.

## Ethical and operational considerations

This is a classroom prototype, not a production security control. Network data
can contain sensitive information. Obtain authorization, minimize retained
data, protect exported predictions, and document dataset bias. Human analysts
must review alerts; model output should not automatically block users or
attribute malicious intent. Monitor drift, false positives, false negatives,
and performance across different environments.

## Dataset attribution

The CSVs are NSL-KDD-style intrusion-detection data supplied with the project.
They represent simulated traffic and should not be interpreted as current
real-world attack prevalence.
