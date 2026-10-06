-- ADY201m: T-SQL queries for SQL Server 2019 (run in SSMS against CardioDB)
-- Q01-Q10 cover the ten API tasks in the brief; Q11-Q13 reproduce the extra console queries.
-- AGE is stored in days; queries convert it with integer division instead of UPDATE so the table stays identical to the source.
USE CardioDB;
GO

-- Q01: Total number of records
SELECT COUNT(*) AS TOTAL_ROWS FROM dbo.CARDIO_TRAIN;

-- Q02: Number of cardiovascular disease cases
SELECT COUNT(*) AS DISEASE_CASES FROM dbo.CARDIO_TRAIN WHERE CARDIO = 1;

-- Q03: Women and men in the study
SELECT GENDER, CASE GENDER WHEN 1 THEN 'Women' ELSE 'Men' END AS LABEL, COUNT(*) AS PEOPLE, AVG(CAST(HEIGHT AS FLOAT)) AS AVG_HEIGHT FROM dbo.CARDIO_TRAIN GROUP BY GENDER ORDER BY GENDER;

-- Q04: 10 highest systolic pressures (AP_HI)
SELECT TOP 10 ID, AP_HI, CARDIO FROM dbo.CARDIO_TRAIN ORDER BY AP_HI DESC, ID;

-- Q05: 10 heaviest patients above the average weight
SELECT TOP 10 ID, WEIGHT, CARDIO FROM dbo.CARDIO_TRAIN WHERE WEIGHT > (SELECT AVG(WEIGHT) FROM dbo.CARDIO_TRAIN) ORDER BY WEIGHT DESC, ID;

-- Q06: 10 patients with above-normal glucose (GLUC > 1)
SELECT TOP 10 ID, GLUC, CARDIO FROM dbo.CARDIO_TRAIN WHERE GLUC > 1 ORDER BY ID;

-- Q07: 10 oldest patients
SELECT TOP 10 ID, AGE / 365 AS AGE_YEARS, CARDIO FROM dbo.CARDIO_TRAIN ORDER BY AGE DESC, ID;

-- Q08: 10 patients with CHOLESTEROL = 3
SELECT TOP 10 ID, CHOLESTEROL, CARDIO FROM dbo.CARDIO_TRAIN WHERE CHOLESTEROL = 3 ORDER BY ID;

-- Q09: 10 smokers
SELECT TOP 10 ID, SMOKE, CARDIO FROM dbo.CARDIO_TRAIN WHERE SMOKE = 1 ORDER BY ID;

-- Q10: 10 physically active patients
SELECT TOP 10 ID, ACTIVE, CARDIO FROM dbo.CARDIO_TRAIN WHERE ACTIVE = 1 ORDER BY ID;

-- Q11: 10 lowest diastolic pressures (AP_LO)
SELECT TOP 10 ID, AP_LO, CARDIO FROM dbo.CARDIO_TRAIN ORDER BY AP_LO, ID;

-- Q12: 10 patients who drink alcohol
SELECT TOP 10 ID, ALCO, CARDIO FROM dbo.CARDIO_TRAIN WHERE ALCO = 1 ORDER BY ID;

-- Q13: Preview with AGE converted from days to years
SELECT TOP 10 ID, AGE AS AGE_DAYS, AGE / 365 AS AGE_YEARS, GENDER, CARDIO FROM dbo.CARDIO_TRAIN ORDER BY ID;

