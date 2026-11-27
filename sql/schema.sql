-- SupportDesk: Customer Support Ticket and SLA Analytics
CREATE DATABASE IF NOT EXISTS supportdesk;
USE supportdesk;

DROP TABLE IF EXISTS tickets;
DROP TABLE IF EXISTS sla;
DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  customer_id   INT PRIMARY KEY AUTO_INCREMENT,
  customer_name VARCHAR(100) NOT NULL,
  email         VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE agents (
  agent_id   INT PRIMARY KEY AUTO_INCREMENT,
  agent_name VARCHAR(100) NOT NULL,
  team       VARCHAR(50)  NOT NULL
);

CREATE TABLE sla (
  sla_id           INT PRIMARY KEY AUTO_INCREMENT,
  priority         VARCHAR(10) NOT NULL UNIQUE,
  response_hours   INT NOT NULL,
  resolution_hours INT NOT NULL
);

CREATE TABLE tickets (
  ticket_id     INT PRIMARY KEY AUTO_INCREMENT,
  customer_id   INT NOT NULL,
  agent_id      INT NOT NULL,
  issue         VARCHAR(200) NOT NULL,
  priority      VARCHAR(10)  NOT NULL,
  status        VARCHAR(20)  NOT NULL,
  created_at    DATETIME     NOT NULL,
  responded_at  DATETIME NULL,
  resolved_at   DATETIME NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (agent_id)    REFERENCES agents(agent_id),
  FOREIGN KEY (priority)    REFERENCES sla(priority)
);
