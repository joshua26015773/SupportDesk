"""SupportDesk demo - follows the live demo plan from the presentation.

Usage:
    python main.py setup    # create database, tables and sample data (+ Mongo comments)
    python main.py demo     # run the full demo
    python main.py report   # only the SQL/pandas report and charts
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import comments
from db import ROOT, query_df, run_sql_file
from report import run_report
from tickets import add_ticket


def setup():
    run_sql_file(ROOT / "sql" / "schema.sql")
    run_sql_file(ROOT / "sql" / "sample_data.sql")
    print("MySQL: database, tables and sample data created.")
    try:
        comments.seed_comments()
        print("MongoDB: sample comments added.")
    except Exception as exc:
        print(f"MongoDB skipped ({exc.__class__.__name__}). Start MongoDB or set MONGO_MOCK=1.")


def demo():
    print("--- 1. Tables ---")
    for table in ("customers", "agents", "sla", "tickets"):
        print(f"\n[{table}]")
        print(query_df(f"SELECT * FROM {table} LIMIT 5").to_string(index=False))

    print("\n--- 2. Insert a sample support ticket ---")
    new_id = add_ticket(customer_id=5, agent_id=3, issue="Cannot upload attachment", priority="Medium")
    print("New ticket created with id:", new_id)

    print("\n--- 3. Ticket status summary query ---")
    print(query_df("SELECT status, COUNT(*) AS total FROM tickets GROUP BY status").to_string(index=False))

    print("\n--- 4. Python report ---")
    run_report()

    print("\n--- 5. Ticket comment from MongoDB (ticket 2) ---")
    try:
        if os.getenv("MONGO_MOCK") == "1":
            comments.seed_comments()  # in-memory mock does not persist between runs
        for doc in comments.get_comments(2):
            print(doc)
    except Exception as exc:
        print(f"MongoDB not available ({exc.__class__.__name__}).")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    {"setup": setup, "demo": demo, "report": run_report}.get(cmd, demo)()
