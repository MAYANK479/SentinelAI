-- Insert default roles
INSERT INTO roles (name) VALUES ('ROLE_ADMIN'), ('ROLE_ANALYST'), ('ROLE_SYSTEM');

-- Insert default admin user (password: admin123)
-- BCrypt hash for admin123 is $2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HCGz5A1OvoYc2e5lJ7e.y
INSERT INTO users (username, password_hash, email) VALUES 
('admin', '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HCGz5A1OvoYc2e5lJ7e.y', 'admin@sentinel.ai'),
('analyst1', '$2a$10$dXJ3SW6G7P50lGmMkkmwe.20cQQubK3.HCGz5A1OvoYc2e5lJ7e.y', 'analyst1@sentinel.ai');

INSERT INTO user_roles (user_id, role_id) VALUES 
((SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM roles WHERE name = 'ROLE_ADMIN')),
((SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM roles WHERE name = 'ROLE_ANALYST')),
((SELECT id FROM users WHERE username = 'analyst1'), (SELECT id FROM roles WHERE name = 'ROLE_ANALYST'));

-- Insert default rules
INSERT INTO fraud_rules (name, description, condition_expression, weight) VALUES 
('High Amount', 'Transaction amount exceeds $1000', 'tx.amount > 1000', 30.0),
('Extreme Velocity', 'More than 10 transactions in a short period', 'tx.velocity > 10', 40.0),
('Geographic Jump', 'Impossible travel time between transactions', 'tx.geoJump == 1', 50.0),
('New Device + High Value', 'New device used for a high value transaction', 'tx.newDevice == 1 && tx.amount > 500', 45.0),
('VPN Used', 'Transaction routed through a VPN or proxy', 'tx.vpnUsed == 1', 20.0),
('High Spend Deviation', 'Amount is >4x the historical average', 'tx.spendDeviation > 4.0', 35.0),
('Multiple Failed Attempts', '>= 3 failed PIN/CVV attempts prior', 'tx.failedAttempts >= 3', 50.0);
