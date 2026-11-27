USE supportdesk;

INSERT INTO customers (customer_name, email) VALUES
('Asha Verma','asha@example.com'),('Rahul Nair','rahul@example.com'),
('Meena Iyer','meena@example.com'),('Karthik Raj','karthik@example.com'),
('Sara Khan','sara@example.com'),('Vikram Singh','vikram@example.com');

INSERT INTO agents (agent_name, team) VALUES
('Priya','Technical'),('Arjun','Billing'),('Divya','Technical'),('Imran','Accounts');

INSERT INTO sla (priority, response_hours, resolution_hours) VALUES
('High',1,8),('Medium',4,24),('Low',8,72);

INSERT INTO tickets (customer_id, agent_id, issue, priority, status, created_at, responded_at, resolved_at) VALUES
(1,1,'Cannot log in to account','High','Closed','2026-11-01 09:00:00','2026-11-01 09:30:00','2026-11-01 14:00:00'),
(2,2,'Charged twice for subscription','High','Closed','2026-11-01 10:00:00','2026-11-01 12:00:00','2026-11-02 10:00:00'),
(3,3,'App crashes on startup','Medium','Closed','2026-11-02 11:00:00','2026-11-02 13:00:00','2026-11-03 09:00:00'),
(4,4,'Update email address','Low','Closed','2026-11-02 15:00:00','2026-11-02 20:00:00','2026-11-04 10:00:00'),
(5,1,'Password reset email not received','Medium','Resolved','2026-11-03 09:30:00','2026-11-03 15:30:00','2026-11-04 12:00:00'),
(6,2,'Invoice download error','Low','In Progress','2026-11-04 10:00:00','2026-11-04 12:00:00',NULL),
(1,3,'Slow dashboard loading','Medium','In Progress','2026-11-05 08:00:00','2026-11-05 09:00:00',NULL),
(2,1,'Data export failing','High','Open','2026-11-06 09:00:00',NULL,NULL),
(3,4,'Change account name','Low','Open','2026-11-06 11:00:00',NULL,NULL),
(4,3,'Payment gateway timeout','High','Closed','2026-11-07 13:00:00','2026-11-07 13:20:00','2026-11-07 20:00:00');
