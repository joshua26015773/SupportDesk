"""Insert a new support ticket. Run directly for a command-line example."""
import argparse
from datetime import datetime

from db import get_connection


def add_ticket(customer_id, agent_id, issue, priority):
    """Create a new 'Open' ticket and return its ticket_id."""
    if priority not in ("High", "Medium", "Low"):
        raise ValueError("priority must be High, Medium or Low")
    sql = (
        "INSERT INTO tickets (customer_id, agent_id, issue, priority, status, created_at) "
        "VALUES (%s, %s, %s, %s, 'Open', %s)"
    )
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(sql, (customer_id, agent_id, issue, priority, datetime.now()))
        return cur.lastrowid


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Add a support ticket")
    p.add_argument("--customer", type=int, required=True, help="customer_id")
    p.add_argument("--agent", type=int, required=True, help="agent_id")
    p.add_argument("--issue", required=True)
    p.add_argument("--priority", choices=["High", "Medium", "Low"], required=True)
    a = p.parse_args()
    print("Created ticket", add_ticket(a.customer, a.agent, a.issue, a.priority))
