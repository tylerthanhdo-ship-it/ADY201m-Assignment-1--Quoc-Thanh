# ADY201m — Cardiovascular disease: analysis and prediction

Coursework for ADY201m: 70,000 patient records stored in a SQL database, queried from Python, explored with statistical tests and classified with machine-learning models (target `CARDIO`).

## Scope and execution status

**Approved alternative:** Microsoft SQL Server 2022 (managed with SSMS), the `pyodbc` API and local Jupyter replace IBM Db2 on Cloud, `ibm_db` and Watson Studio.

| Part | Status |
|---|---|
| Notebook 02 — EDA, statistics, models | Executed locally; all outputs, figures and result files are included. |
| Notebook 01 — | Notebook 01 — SQL Server storage and queries | Executed on SQL Server 2022 (.\SQLEXPRESS); outputs saved in the notebook and results/. |

## Data

| Property | Value |
|---|---:|
| Records | 70,000 |
| Columns | 13 |
| Input features | 11 |
| `CARDIO = 1` | 34,979 (50.0 %) |
| `CARDIO = 0` | 35,021 |

`ID` is a record identifier and is never used as a feature. `AGE` is stored in days; the analysis converts it once with `AGE // 365`.

| File | Content |
|---|---|
| `data/cardio_train_raw.csv` | Source data, `;` separator, age in days. Input for both notebooks. |
| `data/cardio_train_clean.csv` | Age in years, blood pressure capped with full-data IQR limits. EDA/statistics only. |
| `data/CARDIO_TRAIN_export.csv` | Table read back from SQL Server (created by notebook 01). |

Notebook 02 reads the **raw** file rather than the cleaned one, so age is never converted twice and no full-data IQR limits leak into model training.

## Repository structure

```text
.
├── 01_SQLServer_SQL_Python.ipynb   SQL Server table, Q01–Q13 via pyodbc, export, persistence check
├── 02_Cardio_Analysis_ML.ipynb     EDA, IQR cleaning, statistical tests, OLS, models (executed)
├── 02_Cardio_Analysis_ML.html      Browser view of notebook 02
├── ADY201m_Report.html             Self-contained report with all figures and tables
├── cardio_utils.py                 Column lists, raw-data loader, IQRClipper transformer
├── sqlserver_storage.py            Create / load once / verify the SQL Server table
├── requirements.txt                Pinned library versions
├── .env.example                    Connection settings template (no secrets)
├── data/                           Raw, cleaned and exported CSV files
├── sql/                            DDL, SSMS load script, Q01–Q13 (T-SQL), queries.json
├── figures/                        Nine figures from notebook 02
├── results/                        Statistics, model comparison, predictions, saved model
└── MANIFEST.json                   Size and SHA-256 of every file
```

`ADY201m_Report.html` and `02_Cardio_Analysis_ML.html` open directly in a browser; the `.ipynb` files render on GitHub.

## Method

1. Load the raw CSV, validate columns and IDs, and check missing values, duplicates, class balance and impossible blood-pressure readings.
2. Create `dbo.CARDIO_TRAIN` in SQL Server with a primary key on `ID` and CHECK constraints on every coded column. Import the CSV once; later runs compare every stored row with the source instead of reloading.
3. Run 13 T-SQL queries (Q01–Q10 = the ten API tasks in the brief, Q11–Q13 = the extra console queries). Every row-limited query uses `TOP 10` with a full `ORDER BY` so results are deterministic.
4. Explore the data: class balance, histograms, correlation heatmaps, disease rate by feature group, box plots.
5. Cap AP_HI / AP_LO outliers with the IQR rule; run ANOVA, Levene + Welch t-test, Pearson and chi-square tests with effect sizes, and an OLS model.
6. Split 70/30 (49,000 / 21,000), stratified on `CARDIO`, `random_state = 42`.
7. Compare a majority-class baseline, RidgeClassifier, Random Forest, Extra Trees, AdaBoost, Bagging KNN, Gradient Boosting and Stacking.
8. Tune Gradient Boosting with `GridSearchCV` (8 combinations × 3 folds) and select the final model by **cross-validated accuracy on the training set**; the test set is used once to report it.

Every model is a pipeline `IQRClipper → StandardScaler → classifier`, so the IQR limits and scaling parameters are learned from training data only, including inside each cross-validation fold.

## Results

The selected model is **tuned Gradient Boosting** (`learning_rate = 0.05`, `max_depth = 4`, `n_estimators = 200`), CV accuracy **73.64 %**.

| Test-set metric | Value |
|---|---:|
| Accuracy | 73.36 % |
| Precision | 75.25 % |
| Recall | 69.57 % |
| F1-score | 72.30 % |
| ROC-AUC | 80.03 % |

The main risk factors are **systolic blood pressure, cholesterol and age**, consistent across the cleaned correlations, hypothesis tests, OLS and permutation importance. Alcohol shows no significant effect (p ≈ 0.055). Full tables are in `results/` (`model_comparison.csv`, `grid_search.csv`, `statistical_tests.csv`, `feature_importance.csv`, …).

### Expected SQL results (Q01–Q13)

| Query | Result |
|---|---|
| Q01 Total records | 70,000 |
| Q02 Disease cases | 34,979 |
| Q03 Women (GENDER 1) / men (GENDER 2) | 45,530 / 24,470 |
| Q04 Top 10 AP_HI | 8/10 with disease |
| Q05 Top 10 heaviest above average | 8/10 |
| Q06 First 10 with GLUC > 1 | 5/10 |
| Q07 10 oldest | 9/10 |
| Q08 First 10 with CHOLESTEROL = 3 | 9/10 |
| Q09 First 10 smokers | 7/10 |
| Q10 First 10 active | 3/10 |
| Q11 10 lowest AP_LO | 5/10 |
| Q12 First 10 drinkers | 5/10 |
| Q13 Age preview | 4/10 |

Q07 differs from the brief's example (7/10) because it orders by exact age in days; the brief orders after rounding to years, where many patients tie at 64.

## Requirement checklist

| Requirement | Evidence | Status |
|---|---|---|
| Understand and check the dataset | Notebook 02 §1; `results/data_quality.json` | Done |
| Create table, load data, run SQL | `sql/01_create_table.sql`, `sql/02_load_data_ssms.sql`, `sql/03_queries.sql` | Done (SQL Server, approved alternative) |
| Connect from Python and run the 10 queries | Notebook 01 (`pyodbc`) | Code complete — run once on your server |
| Export CSV and close the connection | Notebook 01 §4 | Code complete — run once on your server |
| EDA, IQR cleaning, tests, OLS | Notebook 02 §2–4 | Executed |
| Train and compare models | Notebook 02 §5; `results/model_comparison.csv` | Executed |
| Fine-tune a model | Notebook 02 §5; `results/grid_search.csv` | Executed |
| Notebook environment (instead of Watson Studio) | Local Jupyter | Executed |
| Upload to GitHub | This repository | Push after running notebook 01 |

## Reproduce locally

Requirements: Python 3.11+, SQL Server 2022 (Developer or Express) with SSMS, and [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

```bash
python -m pip install -r requirements.txt
python -m notebook
```

1. Set the connection settings (see `.env.example`). With nothing set, the notebook connects to `localhost` with Windows authentication. A named instance looks like `localhost\SQLEXPRESS`:
   ```bat
   set MSSQL_SERVER=localhost\SQLEXPRESS
   ```
   For a SQL login, also set `MSSQL_UID` and `MSSQL_PWD`.
2. Run notebook 01 (**Restart & Run All**). It creates `CardioDB` and the table on the first run and only verifies them on later runs.
3. Run notebook 02 (**Restart & Run All**), about 3 minutes.
4. Optional: `jupyter nbconvert --to html 01_SQLServer_SQL_Python.ipynb` for a browser copy.

If the notebook reports *Data source name not found*, it prints the installed drivers — set `MSSQL_DRIVER` to one of them (for example `ODBC Driver 17 for SQL Server`).

`cardio_utils.py` must be importable to load `results/cardio_classifier.joblib`; library versions are in `requirements.txt` and `results/environment_versions.csv`.

## Check the stored database

In SSMS:

```sql
USE CardioDB;
SELECT COUNT(*) AS TOTAL_ROWS, SUM(CAST(CARDIO AS INT)) AS DISEASE_CASES FROM dbo.CARDIO_TRAIN;
DBCC CHECKTABLE('dbo.CARDIO_TRAIN');
```

Expected: `70000`, `34979`, and *DBCC execution completed* with no errors. `sql/03_queries.sql` runs Q01–Q13 directly.

## Limitations

- The tests measure association in observational data, not causation; with 70,000 rows, p-values must be read together with effect sizes.
- OLS reproduces the brief's statistics step; the final classifiers handle the binary target.
- Rows that repeat another row's measurements keep their own `ID` and are treated as different patients.
- SMOKE, ALCO and ACTIVE are self-reported; some implausible heights/weights remain after blood-pressure capping.
- Results can differ slightly from the brief's examples because of query ordering, the split and library versions.
- The model is for coursework only and has not been validated for clinical use.

## References

- ADY201m assignment brief and the supplied `cardio_train_raw` dataset ([Kaggle source](https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset)).
- [Microsoft — Python SQL driver (pyodbc)](https://learn.microsoft.com/sql/connect/python/pyodbc/python-sql-driver-pyodbc).
- [Microsoft — BULK INSERT (Transact-SQL)](https://learn.microsoft.com/sql/t-sql/statements/bulk-insert-transact-sql).
- [Microsoft — TOP (Transact-SQL)](https://learn.microsoft.com/sql/t-sql/queries/top-transact-sql).
- [scikit-learn — Common pitfalls and data leakage](https://scikit-learn.org/stable/common_pitfalls.html).
