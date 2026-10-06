# Data files

| File | Content |
|---|---|
| `cardio_train_raw.csv` | Source data supplied with the assignment: 70,000 records, 13 columns, `;` separator, `AGE` in days. Input for both notebooks. |
| `cardio_train_clean.csv` | Written by notebook 02: `AGE` in years and AP_HI/AP_LO capped with full-data IQR limits. For EDA and statistics only — **not** used to train models and not a substitute for the raw file. |
| `CARDIO_TRAIN_export.csv` | Written by notebook 01 when it runs: the table read back from SQL Server, `,` separator, `AGE` in days. |

The SQL Server database itself (`CardioDB`, table `dbo.CARDIO_TRAIN`) lives on your SQL Server instance; notebook 01 or `sql/02_load_data_ssms.sql` creates it.
