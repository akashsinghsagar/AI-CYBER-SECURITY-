# AI-Driven Cyber Threat Awareness and Detection Prototype

## Dataset name

The project uses **NSL-KDD-style network intrusion-detection data**. The
dataset files supplied with the project are:

- `Train_data.csv` - 25,192 labeled network connections.
- `Test_data.csv` - 22,544 unlabeled network connections for optional
  prediction export.

The training file has **42 columns**: 41 network-connection features and the
`class` target column. The test file has the same 41 features but does not
contain the target column.

The target classes are:

- `normal` - normal network traffic.
- `anomaly` - suspicious or attack-related traffic.

The data is derived from the NSL-KDD intrusion-detection dataset and
represents simulated traffic. It should be used for educational analysis,
not as a direct representation of current real-world attack prevalence.

## Project objective

The objective was to build an educational AI-based network intrusion-detection
prototype that:

1. Examines the network-traffic data through exploratory data analysis (EDA).
2. Identifies useful numerical and categorical traffic features.
3. Preprocesses mixed-type network data safely.
4. Trains classification models to distinguish normal traffic from anomalies.
5. Evaluates the models using security-relevant classification metrics.
6. Produces visualizations, metrics, and predictions that can be reviewed by
   an analyst.

## Work completed in the notebook

The exploratory notebook, `Network_intrusion_detection.ipynb`, was used to
load and inspect the training and test CSV files. The training data contains
features such as:

- Connection duration and protocol information.
- Service and connection flag.
- Source and destination byte counts.
- Login, shell, root, and compromise indicators.
- Connection counts and error rates.
- Host-level service and error-rate statistics.

The notebook work included:

- Importing the data with pandas.
- Inspecting the first records, shape, columns, and data types.
- Separating features from the `class` target.
- Encoding categorical values such as protocol, service, and flag.
- Splitting labeled data into training and test/validation portions.
- Scaling numerical features where required.
- Applying feature-selection experimentation with recursive feature
  elimination (RFE).
- Training and comparing classical machine-learning classifiers, including
  K-nearest neighbors, logistic regression, decision tree, random forest,
  AdaBoost, gradient boosting, voting-based classification, Naive Bayes,
  support-vector classification, and other boosting implementations present
  in the notebook.
- Calculating accuracy, error rate, sensitivity/recall, specificity, and
  F1-score.
- Generating confusion matrices and classification reports.
- Comparing model results in summary tables and charts.

The notebook also contains a linear support-vector-machine experiment using
`SVC(kernel="linear", random_state=0)`.

## Reproducible analysis pipeline

The cleaned, repeatable implementation is in
`src/analysis_pipeline.py`. It performs the following steps:

### 1. Locate and load the data

The script searches for `Train_data.csv` and `Test_data.csv` in the `data/`
directory first and then at the project root. The paths can also be supplied
explicitly through command-line arguments.

### 2. Validate the target

The script checks that the training data contains the `class` column. The
target values are converted to lowercase strings and whitespace is removed.

### 3. Split the labeled data

The labeled training data is split into:

- 80% training data.
- 20% validation data.

The split is stratified so that the `normal` and `anomaly` classes remain
represented in similar proportions. A fixed random state of `42` is used for
reproducibility.

### 4. Preprocess the features

The pipeline separates numerical and categorical columns:

- Numerical values are median-imputed and standardized with
  `StandardScaler`.
- Categorical values are filled with the most frequent category and converted
  using one-hot encoding.
- Unknown categories are ignored during transformation.

All learned preprocessing steps are kept inside scikit-learn pipelines. This
prevents information from the validation data from leaking into training.

### 5. Train the models

The reproducible script trains two models on the same processed data:

#### Logistic Regression

This is the fast, transparent baseline model. It provides a useful reference
for judging whether the neural-network prototype offers an improvement.

#### MLP Neural Network

This is a small multilayer perceptron with hidden layers of 32 and 16 units.
It is configured as a prototype with a maximum of 50 iterations and a fixed
random state.

Training time is recorded for both models.

### 6. Evaluate the models

Predictions on the validation split are evaluated using:

- Accuracy.
- Precision for the `anomaly` class.
- Recall for the `anomaly` class.
- F1-score for the `anomaly` class.
- Full classification report.
- Confusion matrix with the order `normal`, `anomaly`.
- Training time in seconds.

Recall is especially important for an intrusion-detection system because it
measures how many anomalies are detected. Precision is also important because
false alarms increase the workload for security analysts.

### 7. Retrain and export predictions

After validation, each model is fitted again on all labeled training data.
The resulting models generate predictions for the unlabeled `Test_data.csv`
file. These predictions are exported for analyst review and are not scored,
because the test file has no ground-truth labels.

## Generated outputs

Running the pipeline creates an `outputs/` directory containing:

- `class_distribution.png` - counts of normal and suspicious events.
- `feature_distributions.png` - distributions of selected attack-related
  features such as `src_bytes`, `dst_bytes`, `count`, and `serror_rate`.
- `threat_indicators.png` - the fraction of suspicious events containing
  indicators such as failed logins, compromised accounts, root shells, or
  attempted `su` access.
- `model_metrics.csv` - accuracy, precision, recall, F1-score, and training
  time for each reproducible model.
- `detailed_metrics.json` - detailed classification reports and confusion
  matrices.
- `logistic_regression_test_predictions.csv` - logistic-regression
  predictions for `Test_data.csv`.
- `mlp_neural_network_test_predictions.csv` - neural-network predictions for
  `Test_data.csv`.

## How to run the project

From the project directory on Windows:

```powershell
py -3.10 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\src\analysis_pipeline.py
```

If virtual-environment activation is blocked, run the interpreter directly:

```powershell
.\venv\Scripts\python.exe .\src\analysis_pipeline.py
```

## Main conclusions

- The project demonstrates a complete educational intrusion-detection
  workflow, from data inspection through prediction export.
- The NSL-KDD-style data contains both categorical and numerical network
  features, so mixed-type preprocessing is necessary.
- A leakage-safe scikit-learn pipeline makes the model comparison more
  reliable and reproducible.
- Logistic Regression provides a simple baseline, while the MLP provides a
  small nonlinear deep-learning comparison.
- Accuracy alone is not enough for security decisions. Recall, precision,
  F1-score, false positives, and false negatives must all be considered.

## Limitations and responsible use

This is a classroom prototype and not a production security control. Model
outputs should not automatically block users, label people as malicious, or
replace human investigation. Before operational use, the system would need
representative current network data, threshold tuning, drift monitoring,
security review, privacy protection, and testing across different
environments.

