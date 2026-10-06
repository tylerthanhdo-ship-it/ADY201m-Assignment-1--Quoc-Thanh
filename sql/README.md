# SQL scripts (SQL Server 2019)

| File | Purpose |
|---|---|
| `01_create_table.sql` | DDL for `dbo.CARDIO_TRAIN`: primary key on `ID` and CHECK constraints on every coded column. Notebook 01 runs it when the table does not exist. |
| `02_load_data_ssms.sql` | Optional manual route in SSMS: creates `CardioDB` and the table, then `BULK INSERT`s the raw CSV (`;` separator). Skips the load if the table already exists. |
| `03_queries.sql` | Q01–Q13 in T-SQL, ready to run in SSMS. |
| `queries.json` | The same 13 queries as data. Notebook 01 reads this file, so the notebook and the SSMS script can never drift apart. |

T-SQL notes: `TOP n` replaces `LIMIT n`; every row-limited query has a full `ORDER BY` (with `ID` as tie-breaker) so results are deterministic; `AGE / 365` is integer division because `AGE` is `INT`.
