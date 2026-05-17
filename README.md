# Human_Liver_Biomarkers
This project investigates the relationships between serum biomarkers and liver disease severity in a cohort of adult patients
Human Liver Biomarkers — Statistical Analysis
Dataset: Human Liver Biomarkers — liver enzymes, proteins, and patient clinical metadata Author: Henri-Philippe Konan

Project overview
The analysis moves from raw data to interpretable statistical models through three main stages:

Data cleaning — standardize, validate, and impute missing or invalid values.
Exploratory data analysis (EDA) — describe distributions and correlations.
Statistical modeling — OLS regression for ALT and AST, followed by between-group comparisons and logistic regression for disease stage prediction.
Research questions
#	Question
1	Which serum biomarkers best predict alanine aminotransferase (ALT) activity?
2	Which serum biomarkers best predict aspartate aminotransferase (AST) activity?
3	Do ALT and AST differ significantly across liver disease stages?
4	Does elevated ALT increase the odds of being diagnosed with advanced liver disease?
Dataset variables
Variable	Type	Description
patient_id	ID	Unique patient identifier
age	Continuous	Age in years
sex	Categorical	Male / Female
bmi	Continuous	Body Mass Index (kg/m²)
alt	Continuous	Alanine aminotransferase, U/L
ast	Continuous	Aspartate aminotransferase, U/L
albumin	Continuous	Serum albumin, g/dL
bilirubin	Continuous	Total bilirubin, mg/dL
protein_a–d	Continuous	Protein expression levels (arbitrary units)
liver_status	Ordinal	Disease stage: 0=Healthy, 1=Fibrosis, 2=Cirrhosis, 3=Cancer
