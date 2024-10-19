# Quiz System

## Introduction

This project is a **real-time quiz system** that allows users to join quiz sessions using a unique quiz ID. Multiple users can participate in the same quiz session simultaneously. As users submit answers, their scores are updated in real-time, and a live leaderboard displays the current standings. The system uses **FastAPI** for the backend and **WebSockets** for real-time communication, ensuring a responsive and engaging experience for users.

### Key Features:
- **User Participation**: Join quiz sessions with a unique quiz ID.
- **Real-Time Score Updates**: Scores are updated instantly as users submit answers.
- **Live Leaderboard**: Displays the standings of all participants, updating in real-time.

---

## Prerequisites

To run the project, you'll need the following software installed:

- **Python 3.11+**: Ensure you have Python installed. [Download Python](https://www.python.org/downloads/)
- **FastAPI**: FastAPI framework is used for the backend.
- **Redis**: Used for real-time data management.
- **Docker (Optional)**: Required for deploying the application with Docker containers.
- **PostgreSQL/MySQL/SQLite**: Any database supported by SQLAlchemy.

---

## Installation & Configuration

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hoangtuananh97/quiz
   cd leaderboard
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**:
   - Rename `.env.example` to `.env` and update any environment variables as needed (e.g., `DATABASE_URL`, `REDIS_URL`).
   - Ensure your Redis and database services are running.

---

## Database Setup

1. **Setup the database** (PostgreSQL or another SQLAlchemy-supported database):
   - Ensure the database URL is correctly set in the `.env` file.
   - Run database migrations using Alembic:
     ```bash
     alembic upgrade head
     ```

2. **Seeding Data** (if necessary):
   - To seed initial quiz data or users, you can create custom database scripts and run them after setting up the database.

---

## Running the Application

1. **Start the development server**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the application** in your web browser:
   - Open your browser and go to `http://localhost:8000`.

3. **Doc APIs**
   -  Open your browser and go to `http://localhost:8000/docs`.
---

## Docker Deployment

For deploying the application using Docker, follow these steps:

1. **Build the Docker image**:
   ```bash
   docker build -t quiz-system .
   ```

2. **Run the Docker containers** using Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. **Access the application** via your browser:
   - After the Docker container starts, access the application at `http://localhost:8000`.

---

### **Scalability**

The system is designed with scalability in mind. Key considerations include:

- **Sharding Leaderboard Scores**: For handling a large number of users, scores can be distributed across multiple Redis shards or partitions to balance the load. This allows the system to handle high user traffic and large-scale quiz sessions efficiently.
- **WebSockets**: The use of WebSockets ensures that real-time updates (such as score changes and leaderboard updates) can scale across multiple users without overwhelming the server.
- **Trade-Offs**: The trade-off in using fixed partitioning for the leaderboard is the complexity in managing shards, especially when users' scores cross shard boundaries.

---

### **Performance**

The component is optimized to perform well under heavy load:

- **Redis Caching**: Scores and real-time data are cached in Redis to reduce database load and improve performance when handling high volumes of quiz participation and score updates.
- **Parallel Queries**: For leaderboard queries, the system can fetch scores from multiple shards in parallel, reducing latency for high-priority queries such as fetching the top 10 players.
- **Optimized WebSocket Handling**: The use of non-blocking WebSocket connections ensures that real-time updates are sent with minimal delay even when the system is under load.

---

### **Reliability**

The system is built to handle errors gracefully and ensure reliability:

- **Error Handling**: WebSocket disconnections are detected, and reconnections are managed automatically. Any critical errors are logged for further diagnostics.
- **Resilient to Failures**: Redis is used for real-time data storage, ensuring that even if a node fails, the data can be recovered using Redis Clustering.
- **Transaction Safety**: Database transactions are carefully managed to prevent data inconsistency in scenarios where multiple users are joining the same quiz session or submitting answers simultaneously.

---

### **Maintainability**

The code is structured to be clean and easy to maintain:

- **Modular Design**: The system is divided into modules for WebSockets, score handling, and quiz management, making it easy for other developers to extend or modify the system.
- **Consistent Code Style**: Followed best practices such as using PEP8 for Python code, clear naming conventions, and structured logging to make the codebase understandable and consistent.
- **Clear Separation of Concerns**: Responsibilities for different components (e.g., real-time updates, leaderboard management) are clearly separated, reducing complexity when adding new features.

---

### **Monitoring and Observability**

To ensure the system is observable and easy to monitor:

- **Centralized Logging**: All WebSocket events, database queries, and errors are logged using Python’s logging module. Logs can be aggregated using ELK Stack (Elasticsearch, Logstash, Kibana) for real-time analysis.
- **Performance Metrics**: Tools like Prometheus are used to collect and monitor key metrics such as WebSocket connection counts, message latency, and Redis performance. These metrics are visualized using Grafana dashboards for real-time monitoring.
- **Error Alerts**: Tools like Sentry are used to catch exceptions in real-time, alerting the development team of any critical errors or issues in the system.
---

## Usage

1. **Join a Quiz**:
   - Users can join a quiz by entering their username and a unique quiz ID.
   
2. **Submit Answers**:
   - After joining, participants can submit answers to questions. Their scores will be updated in real-time and displayed on the leaderboard.

3. **Leaderboard**:
   - The leaderboard is automatically updated as participants answer questions. All users can see the current standings in real-time.

---

## Troubleshooting

1. **WebSocket Connection Issues**:
   - **Issue**: WebSocket connection is not established.
   - **Solution**: Ensure WebSocket connections are handled over `ws://localhost:8000` or `wss://` if using HTTPS.

2. **Database Migrations**:
   - **Issue**: Migration scripts fail to run.
   - **Solution**: Ensure the `DATABASE_URL` is correctly set in your `.env` file and that the database service is running.

3. **Redis Connection Errors**:
   - **Issue**: Cannot connect to Redis.
   - **Solution**: Verify that Redis is running and the `REDIS_URL` is set correctly in the `.env` file.
