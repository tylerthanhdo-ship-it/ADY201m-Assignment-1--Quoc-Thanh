"""Create, load and verify the CARDIO_TRAIN table on Microsoft SQL Server 2022."""
import os
from pathlib import Path

import pandas as pd
import pyodbc

from cardio_utils import COLUMNS

DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"


def settings_from_env():
    return {
        "server": os.getenv("MSSQL_SERVER", "localhost"),
        "database": os.getenv("MSSQL_DATABASE", "CardioDB"),
        "uid": os.getenv("MSSQL_UID", ""),
        "pwd": os.getenv("MSSQL_PWD", ""),
        "driver": os.getenv("MSSQL_DRIVER", DEFAULT_DRIVER),
    }


def connection_string(settings, database=None):
    auth = f"UID={settings['uid']};PWD={settings['pwd']};" if settings["uid"] else "Trusted_Connection=yes;"
    return (f"DRIVER={{{settings['driver']}}};SERVER={settings['server']};"
            f"DATABASE={database or settings['database']};{auth}"
            "Encrypt=yes;TrustServerCertificate=yes;")


def ensure_database(settings):
    with pyodbc.connect(connection_string(settings, "master"), autocommit=True) as master:
        name = settings["database"]
        master.execute(f"IF DB_ID(N'{name}') IS NULL CREATE DATABASE [{name}]")


def table_exists(connection, table="CARDIO_TRAIN"):
    return connection.execute("SELECT OBJECT_ID(?, 'U')", f"dbo.{table}").fetchval() is not None


def read_table(connection, table="CARDIO_TRAIN"):
    cursor = connection.execute(f"SELECT {', '.join(COLUMNS)} FROM dbo.{table} ORDER BY ID")
    frame = pd.DataFrame.from_records(cursor.fetchall(), columns=COLUMNS)
    frame["WEIGHT"] = frame["WEIGHT"].astype(float)
    return frame


def open_cardio_database(source, settings, ddl_path, batch_size=5000):
    """Import the source once; on later runs verify the stored rows instead of reloading them.

    An existing but empty table (e.g. created by a manual SSMS script whose load failed) is filled.
    Returns (connection, created) where created is True when rows were imported in this call.
    """
    ensure_database(settings)
    connection = pyodbc.connect(connection_string(settings))
    try:
        exists = table_exists(connection)
        empty = exists and connection.execute("SELECT COUNT(*) FROM dbo.CARDIO_TRAIN").fetchval() == 0
        created = not exists or empty
        if created:
            cursor = connection.cursor()
            if not exists:
                cursor.execute(Path(ddl_path).read_text(encoding="utf-8"))
            cursor.fast_executemany = True
            insert = (f"INSERT INTO dbo.CARDIO_TRAIN ({', '.join(COLUMNS)}) "
                      f"VALUES ({', '.join('?' for _ in COLUMNS)})")
            rows = [tuple(int(v) if i != 4 else float(v) for i, v in enumerate(r))
                    for r in source[COLUMNS].itertuples(index=False, name=None)]
            for start in range(0, len(rows), batch_size):
                cursor.executemany(insert, rows[start:start + batch_size])
            connection.commit()
        verify_against_source(connection, source)
        return connection, created
    except Exception:
        connection.rollback()
        connection.close()
        raise


def verify_against_source(connection, source):
    stored = read_table(connection)
    expected = source[COLUMNS].reset_index(drop=True)
    pd.testing.assert_frame_equal(stored, expected, check_dtype=False)
    connection.execute("DBCC CHECKTABLE('dbo.CARDIO_TRAIN') WITH NO_INFOMSGS")
    return True
