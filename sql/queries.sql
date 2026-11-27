USE supportdesk;

-- 1. Tickets by status
SELECT status, COUNT(*) AS total FROM tickets GROUP BY status;

-- 2. Tickets by priority
SELECT priority, COUNT(*) AS total FROM tickets GROUP BY priority ORDER BY total DESC;

-- 3. Workload per agent
SELECT a.agent_name, a.team, COUNT(*) AS tickets_handled
FROM tickets t JOIN agents a ON a.agent_id = t.agent_id
GROUP BY a.agent_id, a.agent_name, a.team
ORDER BY tickets_handled DESC;

-- 4. Open high-priority tickets
SELECT ticket_id, issue, status, created_at
FROM tickets
WHERE priority = 'High' AND status IN ('Open', 'In Progress');

-- 5. SLA check per ticket (actual time vs target time)
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
FROM tickets t
JOIN sla s ON s.priority = t.priority;
