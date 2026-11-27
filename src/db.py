"""Database helpers: MySQL connection, SQL file runner, and query -> DataFrame."""
import os
from pathlib import Path

import pandas as pd
import pymysql
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

MYSQL = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}
DB_NAME = os.getenv("MYSQL_DATABASE", "supportdesk")


def get_connection(use_database=True):
    """Open a MySQL connection (optionally without selecting the database)."""
    params = dict(MYSQL)
    if use_database:
        params["database"] = DB_NAME
    return pymysql.connect(**params, autocommit=True)


def run_sql_file(path):
    """Execute every statement in a .sql file."""
    text = Path(path).read_text()
    statements = [s.strip() for s in text.split(";") if s.strip()]
    with get_connection(use_database=False) as conn, conn.cursor() as cur:
        for stmt in statements:
            cur.execute(stmt)


def query_df(sql, params=None):
    """Run a SELECT query and return the result as a pandas DataFrame."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        columns = [c[0] for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=columns)
