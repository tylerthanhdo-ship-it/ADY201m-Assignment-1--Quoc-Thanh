# Results

Written by notebook 02 (analysis) unless noted.

| File | Content |
|---|---|
| `data_quality.json` | Row/ID counts, missing values, duplicates, class balance, invalid blood-pressure counts |
| `descriptive_statistics.csv` | `describe()` of all features (AGE in years) |
| `iqr_limits.csv` | Full-data IQR limits and number of capped values (EDA/statistics) |
| `statistical_tests.csv` | ANOVA, Levene, Welch t-test, Pearson, chi-square — statistic, p-value, effect size, decision |
| `ols_summary.txt`, `ols_coefficients.csv` | statsmodels OLS output |
| `grid_search.csv` | 8 Gradient Boosting configurations × 3-fold CV |
| `model_comparison.csv` | CV accuracy and test accuracy/precision/recall/F1/ROC-AUC for all models |
| `feature_importance.csv` | Permutation importance of the selected model on the test set |
| `train_ids.csv`, `test_ids.csv` | Patient IDs in each split (reproducibility) |
| `test_predictions.csv` | ID, true label, predicted label and score for the test set |
| `cardio_classifier.joblib` | Fitted pipeline (IQR capping → scaling → model). Load with `cardio_utils.py` importable and the versions in `environment_versions.csv`. |
| `environment_versions.csv` | Python and library versions used |
| `summary.json` | One-file summary of data quality, split, selection and test metrics |
| `db_execution_status.json` | **Notebook 01.** SQL Server connection, row counts and persistence check |
| `query_summary.csv` | **Notebook 01.** Rows returned and disease cases for Q01–Q13 |
