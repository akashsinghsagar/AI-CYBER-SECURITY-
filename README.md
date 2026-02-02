# Network Intrusion Detection System using Machine Learning

## 📌 Project Overview

This project implements a **machine learning-based Intrusion Detection System (IDS)** to identify malicious network activity (anomalies / intrusions) in real-time or near real-time.  
We use the well-known **NSL-KDD dataset** (improved version of classic KDD Cup 1999) and apply multiple classical and ensemble machine learning algorithms to classify network connections as **normal** or **anomalous**.

### Why this project matters

Cyberattacks are becoming increasingly sophisticated, automated, and frequent. Traditional signature-based IDS struggle with zero-day attacks and polymorphic malware.  
Machine learning offers the ability to:

- Learn complex patterns from data
- Detect previously unseen attack variants (anomaly-based detection)
- Scale to high-volume network traffic
- Reduce false positives over time with better feature engineering and model selection

## 🎯 Objectives

- Build an accurate and efficient ML-based intrusion detection model
- Compare performance of multiple classifiers (Logistic Regression, SVM, Decision Tree, Random Forest, KNN, etc.)
- Apply proper preprocessing, feature selection, and scaling
- Achieve high detection rate while keeping false positives low
- Provide reproducible code and clear documentation

## 🚀 Goals

- Develop a system capable of detecting both **known** and **novel** attack patterns
- Handle high-dimensional network traffic features effectively
- Outperform baseline traditional methods in accuracy, recall, and F1-score
- Create a foundation that can later be extended to deep learning or real-time streaming detection

## 📊 Dataset

**Source**: NSL-KDD (improved KDD Cup 1999 dataset)  
**Files included**:

- `Train_data.csv` → Training set
- `Test_data.csv`   → Testing / evaluation set

**Key characteristics**:

- 41 features (38 numeric + 3 categorical: protocol_type, service, flag)
- Binary target: `normal` vs `anomaly` (originally multi-class attack types collapsed to binary)
- Simulated military network environment with realistic normal traffic + various attack types (DoS, Probe, R2L, U2R)

## 🛠️ Methodology & Preprocessing Pipeline

1. **Data Cleaning**  
   - Checked for missing values (`isnull().sum()`)  
   - Dropped useless / constant column: `num_outbound_cmds`

2. **Categorical Encoding**  
   - `LabelEncoder` applied to: `protocol_type`, `service`, `flag`

3. **Feature Selection**  
   - Recursive Feature Elimination (**RFE**) with `RandomForestClassifier`  
   - Selected top 10 most important features

4. **Feature Scaling**  
   - `StandardScaler` → mean=0, std=1 (important for distance-based models like KNN, SVM)

5. **Train / Validation Split**  
   - `train_test_split` (usually 80/20 or 70/30)

6. **Models Trained & Compared**

   - Logistic Regression
   - Support Vector Machine (SVM)
   - Decision Tree
   - Random Forest
   - K-Nearest Neighbors (KNN)
   - (Others can be easily added: XGBoost, LightGBM, etc.)

7. **Evaluation Metrics**

   - Accuracy
   - Error Rate
   - Sensitivity / Recall
   - Specificity
   - F1 Score

## 📈 Best Results (from notebook)

| Model               | Accuracy   | Error Rate | Sensitivity (Recall) | Specificity | F1 Score   |
|---------------------|------------|------------|-----------------------|-------------|------------|
| Random Forest       | **99.55%** | 0.45%      | 99.55%                | 99.70%      | 99.55%     |
| Decision Tree       | **99.55%** | 0.45%      | 99.55%                | 99.70%      | 99.55%     |
| KNN                 | 98.90%     | 1.10%      | 98.90%                | 99.20%      | 98.90%     |
| Logistic Regression | 97.45%     | 2.55%      | 97.45%                | 98.03%      | 97.45%     |
| SVM                 | 94.27%     | 5.73%      | 94.27%                | 96.11%      | 94.26%     |

**Top performers**: Random Forest & Decision Tree → ~99.55% accuracy on the test set.

## 🏗️ How to Run the Project Locally

```bash
# 1. Clone the repository
git clone https://github.com/Harshr24/Network_intrusion_detection.git
cd Network_intrusion_detection

# 2. (Recommended) Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt   # (create this file if not present)

# Common packages you will need:
# numpy pandas scikit-learn matplotlib seaborn jupyter

# 4. Launch Jupyter Notebook
jupyter notebook

# 5. Open → Network_intrusion_detection.ipynb
# Run all cells sequentially
