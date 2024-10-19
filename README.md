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
