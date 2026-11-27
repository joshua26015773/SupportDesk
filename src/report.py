"""Python report: runs the analytical SQL queries with pandas and saves charts."""
import matplotlib

matplotlib.use("Agg")  # save charts to files, no display needed
import matplotlib.pyplot as plt

from db import ROOT, query_df

OUT = ROOT / "output"

Q_STATUS = "SELECT status, COUNT(*) AS total FROM tickets GROUP BY status ORDER BY total DESC"
Q_PRIORITY = "SELECT priority, COUNT(*) AS total FROM tickets GROUP BY priority ORDER BY total DESC"
Q_AGENT = """
    SELECT a.agent_name, a.team, COUNT(*) AS tickets_handled
    FROM tickets t JOIN agents a ON a.agent_id = t.agent_id
    GROUP BY a.agent_id, a.agent_name, a.team
    ORDER BY tickets_handled DESC"""
Q_HIGH_OPEN = """
    SELECT ticket_id, issue, status, created_at FROM tickets
    WHERE priority = 'High' AND status IN ('Open', 'In Progress')"""
Q_SLA = """
    SELECT t.ticket_id, t.priority,
           ROUND(TIMESTAMPDIFF(MINUTE, t.created_at, t.responded_at) / 60, 2) AS response_hrs,
           s.response_hours AS response_target,
           CASE WHEN t.responded_at IS NULL THEN 'Pending'
                WHEN TIMESTAMPDIFF(MINUTE, t.created_at, t.responded_at) <= s.response_hours * 60
                THEN 'Met' ELSE 'Breached' END AS response_sla,
           ROUND(TIMESTAMPDIFF(MINUTE, t.created_at, t.resolved_at) / 60, 2) AS resolution_hrs,
           s.resolution_hours AS resolution_target,
           CASE WHEN t.resolved_at IS NULL THEN 'Pending'
                WHEN TIMESTAMPDIFF(MINUTE, t.created_at, t.resolved_at) <= s.resolution_hours * 60
                THEN 'Met' ELSE 'Breached' END AS resolution_sla
    FROM tickets t JOIN sla s ON s.priority = t.priority
    ORDER BY t.ticket_id"""


def bar_chart(df, x, y, title, filename):
    ax = df.plot.bar(x=x, y=y, legend=False, rot=0, figsize=(6, 4), color="#2a6f97")
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Tickets")
    for bar in ax.patches:
        ax.annotate(int(bar.get_height()), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=120)
    plt.close()


def sla_summary(sla_df):
    """Percentage of ticket targets met (ignoring tickets still pending)."""
    rows = {}
    for label, col in (("Response", "response_sla"), ("Resolution", "resolution_sla")):
        done = sla_df[sla_df[col] != "Pending"]
        met = (done[col] == "Met").sum()
        rows[label] = f"{met}/{len(done)} met ({100 * met / len(done):.0f}%)" if len(done) else "n/a"
    return rows


def run_report():
    OUT.mkdir(exist_ok=True)
    status, priority = query_df(Q_STATUS), query_df(Q_PRIORITY)
    agents, high_open, sla_df = query_df(Q_AGENT), query_df(Q_HIGH_OPEN), query_df(Q_SLA)

    print("\n=== Tickets by status ===\n", status.to_string(index=False))
    print("\n=== Tickets by priority ===\n", priority.to_string(index=False))
    print("\n=== Workload per agent ===\n", agents.to_string(index=False))
    print("\n=== Open / in-progress HIGH priority tickets ===\n", high_open.to_string(index=False))
    print("\n=== SLA check per ticket ===\n", sla_df.to_string(index=False))
    print("\n=== SLA summary ===")
    for k, v in sla_summary(sla_df).items():
        print(f"{k}: {v}")

    bar_chart(status, "status", "total", "Tickets by Status", "tickets_by_status.png")
    bar_chart(priority, "priority", "total", "Tickets by Priority", "tickets_by_priority.png")
    bar_chart(agents, "agent_name", "tickets_handled", "Tickets per Agent", "tickets_per_agent.png")
    sla_df.to_csv(OUT / "sla_report.csv", index=False)
    print(f"\nCharts and sla_report.csv saved in: {OUT}")


if __name__ == "__main__":
    run_report()
