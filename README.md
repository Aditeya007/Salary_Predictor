# 💻 Software Developer Salary Predictor

A machine learning web application that predicts the **annual salary** of a software developer based on their country, education level, developer role, and years of experience. Built using **Streamlit** and **scikit-learn**, powered by data from the **Stack Overflow Developer Survey**.

---

## 📋 Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Model](#model)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Disclaimer](#disclaimer)

---

## 🎥 Demo

Launch the app and fill in your profile:

| Field               | Options                                                    |
|---------------------|------------------------------------------------------------|
| 🌍 Country           | 39 countries + "Other" (based on survey respondent counts) |
| 🎓 Education Level   | Less than a Bachelor's, Bachelor's, Master's, Post Grad    |
| 💻 Developer Type    | Full-stack, Back-end, Data Scientist, DevOps, and more     |
| 🧑‍💼 Years of Experience | 0–50 years (slider)                                    |

Click **🔮 Predict My Salary** to get an estimated USD annual salary.

---

## ✨ Features

- **Instant salary predictions** powered by a pre-trained Random Forest model
- **Interactive UI** with dropdowns, a slider, and live metric display
- **39+ countries** supported (low-frequency countries are grouped as "Other")
- **Clean & styled output** showing the predicted salary in a formatted card
- **Model caching** for fast repeated predictions without reloading

---

## 🛠️ Tech Stack

| Technology      | Purpose                              |
|-----------------|--------------------------------------|
| Python          | Core language                        |
| Streamlit       | Web framework / UI                   |
| scikit-learn    | Machine learning (Random Forest, preprocessing) |
| NumPy           | Numerical operations                 |
| Pandas          | Data manipulation (notebook only)    |
| Matplotlib / Seaborn | EDA and visualisation (notebook only) |

---

## 📊 Dataset

The model was trained on data from the **Stack Overflow Developer Survey**.

> 📥 **Download the dataset:** The raw CSV is **not included** in this repository due to its size. You can download it for free from the official Stack Overflow survey page:
> **https://survey.stackoverflow.co/**
> Look for the annual *Developer Survey Results* and download `survey_results_public.csv`.
> *(The dataset is only needed if you want to retrain the model. The app ships with a pre-trained `saved_steps2.pkl` and works without the CSV.)*

**Features used:**
| Feature         | Description                              |
|-----------------|------------------------------------------|
| `Country`       | Country where the developer works        |
| `EdLevel`       | Education level (mapped to 4 categories) |
| `YearsCodePro`  | Years of professional coding experience  |
| `DevType`       | Primary developer role / job type        |

**Target variable:** `ConvertedCompYearly` — annual compensation in USD

**Data preprocessing steps:**
1. Selected relevant columns and renamed `ConvertedCompYearly` → `Salary`
2. Dropped rows with missing `Salary` values (65,437 → 23,435 rows)
3. Dropped `WorkExp` column due to ~7,200 missing values
4. Removed remaining rows with nulls (→ 23,321 rows)
5. Converted `YearsCodePro` strings (`"Less than 1 year"` → `0.5`, `"More than 50 years"` → `50`) to floats
6. Applied IQR-based outlier filtering on `Salary` (upper bound: ~$220,619 → 22,349 rows)
7. Grouped countries with fewer than 100 respondents into `"Other"` (39 countries remain)
8. Simplified education levels into 4 categories: `Less than a Bachelors`, `Bachelor's degree`, `Master's degree`, `Post grad`
9. Label-encoded `Country` and `DevType`; ordinal-encoded `EdLevel`

---

## 🤖 Model

Multiple regression models were evaluated:

| Model               | R² Score |
|---------------------|----------|
| Linear Regression   | ~0.226   |
| Lasso               | ~0.226   |
| LassoCV             | ~0.226   |
| Ridge               | ~0.226   |
| RidgeCV             | ~0.226   |
| **Random Forest**   | **~0.510** |

✅ **Random Forest Regressor** was selected as the best model with an R² of ~0.51 on the test set.

A `StandardScaler` is applied to input features before prediction. The trained model, scaler, and label encoders are persisted together in `saved_steps2.pkl`.

---

## 📁 Project Structure

```
project/
├── app.py                  # Streamlit web app
├── salary_pred.ipynb       # Jupyter notebook (EDA, preprocessing, model training)
├── saved_steps2.pkl        # Serialized model + scaler + label encoders
├── requirements.txt        # Python dependencies
├── data/
│   └── survey_results_public.csv   # ⚠️ Not included — download from https://survey.stackoverflow.co/
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+
- pip

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aditeya007/Salary_Predictor.git
   cd Salary_Predictor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the model file is present**

   `saved_steps2.pkl` is included in the repository and is all you need to run the app.

4. **Dataset** *(only needed for retraining the model)*

   The raw survey CSV is **not included** in this repo. To retrain the model:
   - Download `survey_results_public.csv` from **https://survey.stackoverflow.co/**
   - Place it at `data/survey_results_public.csv`
   - Run `salary_pred.ipynb` to preprocess the data and regenerate `saved_steps2.pkl`

---

## 🚀 Usage

Run the Streamlit app from the project root:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## ⚙️ How It Works

1. **User inputs** are collected via the Streamlit UI (country, education, experience, developer type).
2. Inputs are **encoded** using the same `LabelEncoder` objects and education ordinal mapping used during training.
3. The encoded vector is **scaled** using the saved `StandardScaler`.
4. The **Random Forest Regressor** predicts the annual salary in USD.
5. The result is displayed in a styled card.

**Input encoding:**

| Input          | Encoding Method                         |
|----------------|-----------------------------------------|
| Country        | `LabelEncoder` (fitted on training data) |
| Education Level | Ordinal mapping: Less than Bachelor's→0, Bachelor's→1, Master's→2, Post Grad→3 |
| Dev Type       | `LabelEncoder` (fitted on training data) |
| Years Experience | Raw numeric value                     |

---

## ⚠️ Disclaimer

> This is an **estimate** based on Stack Overflow Developer Survey data and may not reflect actual salaries. Predictions are subject to market conditions, geographic factors, company size, individual skills, and negotiation. Use this tool for **informational purposes only**.
