# SentinelAI

SentinelAI is a powerful, real-time fraud detection platform built to analyze transactions using a hybrid approach of heuristic rules and advanced machine learning models (XGBoost and Random Forest).

The system continuously evaluates incoming transaction streams, calculates a composite risk score based on business logic and predictive AI models, and broadcasts the live results to an interactive dashboard via WebSockets.

## Architecture & Tech Stack

SentinelAI is composed of three primary microservices:

1. **AI Service (`/ai-service`) - Python & FastAPI**
   - Serves the machine learning models (XGBoost, Logistic Regression, Random Forest).
   - Provides an `/api/v1/predict` endpoint that evaluates transaction features (Amount, Velocity, Spend Deviation, etc.) and returns a fraud probability.
   - Includes endpoints to dynamically retrain models.

2. **Backend Engine (`/backend`) - Java & Spring Boot**
   - The core orchestration layer.
   - **Transaction Simulator:** Generates continuous mock transactions for monitoring.
   - **Rule Evaluator:** Uses the Spring Expression Language (SpEL) to run dynamic heuristic rules against transactions in real-time.
   - **Composite Risk Engine:** Combines the AI prediction and the heuristic rule score to determine a final composite risk band.
   - **WebSocket Broker:** Streams the evaluation results to the frontend.
   - Persists case data and business rules to PostgreSQL.

3. **Live Dashboard (`/frontend`) - Next.js & React**
   - A stunning, real-time monitoring interface.
   - Connects to the Spring Boot backend via SockJS and STOMP to listen for live transaction events.
   - Displays risk trends, recent transactions, and system health.

## Getting Started

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose

### Running the Platform

To build and start all services (Database, AI Service, Backend, and Frontend), simply run:

```bash
docker compose up -d --build
```

### Accessing the Services

Once the containers are successfully running, you can access the following interfaces:

- **Live Dashboard (Frontend):** [http://localhost:3000](http://localhost:3000)
- **Spring Boot Backend API:** `http://localhost:8080`
- **AI Service (FastAPI Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Key Features

- **Real-Time Processing:** Low latency evaluation of every simulated transaction.
- **Explainability:** The AI model returns feature influences to help human analysts understand exactly *why* a transaction was flagged.
- **Dynamic Rules:** Heuristic rules can be modified without altering the core ML model, making the system highly adaptable to new fraud patterns.
