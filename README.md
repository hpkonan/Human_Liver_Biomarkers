# Human Liver Biomarkers — Statistical Analysis

> Predicting liver enzyme activity and classifying advanced liver disease from serum biomarkers using OLS regression and logistic regression in Python.

---

## Overview

This project investigates the relationships between serum biomarkers and liver disease severity in a cohort of adult patients. The analysis moves from raw clinical data to interpretable statistical models through four stages: data cleaning, exploratory data analysis, OLS regression modelling, and logistic regression for disease stage prediction.

**Dataset**: Human Liver Biomarkers — liver enzymes, proteins, and patient clinical metadata  
**Author**: Henri-Philippe Konan

---

## Research Questions

| # | Question |
|---|---|
| 1 | Which serum biomarkers best predict alanine aminotransferase (ALT) activity? |
| 2 | Which serum biomarkers best predict aspartate aminotransferase (AST) activity? |
| 3 | Do ALT and AST differ significantly across liver disease stages? |
| 4 | Does elevated ALT increase the odds of being diagnosed with advanced liver disease? |

---

## Dataset

| Variable | Type | Description |
|---|---|---|
| `patient_id` | ID | Unique patient identifier |
| `age` | Continuous | Age in years |
| `sex` | Categorical | Male / Female |
| `bmi` | Continuous | Body Mass Index (kg/m²) |
| `alt` | Continuous | Alanine aminotransferase, U/L |
| `ast` | Continuous | Aspartate aminotransferase, U/L |
| `albumin` | Continuous | Serum albumin, g/dL |
| `bilirubin` | Continuous | Total bilirubin, mg/dL |
| `protein_a–d` | Continuous | Protein expression levels (arbitrary units) |
| `liver_status` | Ordinal | Disease stage: 0=Healthy, 1=Fibrosis, 2=Cirrhosis, 3=Cancer |

---

## Methodology

### 1. Data Cleaning
- Standardize column names and remove duplicate patient records
- Impute missing categorical values (`sex` via proportional random sampling, `liver_status` via mode)
- Replace physiologically impossible values (negative ALT/AST) with NaN, then impute by sampling from the observed distribution to preserve right-skewed shape
- Impute remaining continuous variables using mean or median selected automatically based on skewness
- Encode disease stage as an ordinal integer (Healthy=0 → Cancer=3)

### 2. Exploratory Data Analysis
- Univariate distributions of all biomarkers, stratified by sex
- Boxplots of enzyme activity across disease stages
- Pearson correlation heatmap and LOWESS regression plots
- Pairplot (ALT, AST, albumin, bilirubin) and group-level means by disease stage

### 3. OLS Regression (ALT and AST)
ALT and AST are log1p-transformed to correct for right skew and linearize relationships with predictors. An incremental model-building strategy is used:

| Model | Formula (ALT) |
|---|---|
| M1 | `log_alt ~ albumin` |
| M2 | `log_alt ~ albumin + bilirubin` |
| M3 | `log_alt ~ albumin + bilirubin + ast` |
| M4 | `log_alt ~ albumin + bilirubin + ast + sex` (full model) |

Diagnostics: Residuals vs Fitted, Normal Q-Q, Breusch-Pagan heteroscedasticity test, HC3 robust standard errors, Variance Inflation Factor (VIF).

**Key findings**:
- Albumin is the strongest single predictor of ALT (M1 R² = 0.214, negative coefficient)
- Adding bilirubin and AST raises R² to ~0.30
- Sex is not a significant predictor once biochemical markers are controlled for
- Disease stage alone explains 39% of log_alt variance and 48% of log_ast variance

### 4. Between-Group Comparisons
- Levene's test for variance homogeneity
- One-way ANOVA (standard) and Welch ANOVA (when Levene p < 0.05)
- Tukey HSD (log_ast) and Games-Howell post-hoc (log_alt, unequal variances)
- Spearman ρ and Kendall τ rank correlations with liver disease stage

**Key findings**:
- Both enzymes increase significantly with disease stage (ANOVA p < 0.001)
- AST tracks disease progression slightly more tightly than ALT (higher β and R²)
- Albumin is the strongest *negative* predictor of stage (ρ = −0.714)

### 5. Logistic Regression
Binary outcome: Non-advanced (Healthy/Fibrosis) vs Advanced (Cirrhosis/Cancer).

Two models are compared:

| Model | Predictors | AUC |
|---|---|---|
| logit1 | `log_alt` | Reported in notebook |
| logit2 | `log_alt + albumin + bilirubin` | Higher — reported in notebook |

Diagnostics: Odds Ratios with 95% CI, Likelihood Ratio Test, VIF, confusion matrix, ROC curve, Hosmer-Lemeshow calibration test.

---

## Stack

| Library | Use |
|---|---|
| `pandas` / `numpy` | Data manipulation and imputation |
| `matplotlib` / `seaborn` | Visualization |
| `scipy.stats` | ANOVA, Levene, Spearman, Kendall |
| `statsmodels` | OLS, logistic regression, Tukey HSD, Breusch-Pagan, VIF |
| `pingouin` | Welch ANOVA, Games-Howell post-hoc |
| `sklearn` | Confusion matrix, ROC curve, AUC |

---

## Project Structure

```
├── Human_liver_biomarkers.ipynb   # Main analysis notebook
├── src/
│   ├── data_utils.py              # Imputation and summary statistics helpers
│   ├── visualization.py           # Reusable plotting functions
│   └── ols_utils.py               # OLS diagnostics and model comparison utilities
└── Human_Liver_Biomarkers.csv     # Dataset (not included in repo)
```

---

## Limitations

1. `protein_a–d` lack clinical labels, limiting biological interpretation
2. Imputing ALT/AST from the observed distribution may underestimate model uncertainty
3. Logistic models were not cross-validated — AUC estimates are optimistic on training data
4. The 0.5 classification threshold is not clinically optimized
5. Cross-sectional design: causal inference is not warranted

---

## Author

**Henri-Philippe Konan**  
IBM Data Science Professional Certificate · Portfolio project
