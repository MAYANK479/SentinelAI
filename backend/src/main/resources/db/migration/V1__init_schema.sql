CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE user_roles (
    user_id BIGINT REFERENCES users(id),
    role_id BIGINT REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE fraud_rules (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    condition_expression TEXT NOT NULL,
    weight FLOAT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    amount FLOAT,
    merchant_risk FLOAT,
    night_time INT,
    velocity INT,
    geo_jump INT,
    new_device INT,
    vpn_used INT,
    spend_deviation FLOAT,
    failed_attempts INT,
    ml_probability FLOAT,
    rule_score FLOAT,
    behavior_score FLOAT,
    composite_score FLOAT,
    risk_band VARCHAR(20),
    is_fraud INT,
    narrative TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fraud_cases (
    id BIGSERIAL PRIMARY KEY,
    transaction_id BIGINT REFERENCES transactions(id),
    analyst_id BIGINT REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'OPEN', -- OPEN, ASSIGNED, UNDER_INVESTIGATION, RESOLVED, FALSE_POSITIVE
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE case_comments (
    id BIGSERIAL PRIMARY KEY,
    case_id BIGINT REFERENCES fraud_cases(id),
    user_id BIGINT REFERENCES users(id),
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
