# 🎬 High-Concurrency Movie Reservation System (Backend Engine)

A robust, production-grade backend engine designed to handle high-volume ticket bookings during high-demand movie releases. Built with **FastAPI**, **PostgreSQL (SQLAlchemy)**, **Redis**, and **Celery**, this system guarantees **zero double-bookings** under heavy concurrent traffic using pessimistic database row-level locking and upfront Redis traffic shaping.

---

## 🏛️ System Architecture

```mermaid
flowchart TB
    Client["🌐 Incoming Client Traffic"]

    API["⚡ FastAPI Server"]

    Redis["🔴 Redis<br/>Virtual Waiting Room<br/>(Sorted Sets Queue Gate)"]

    DB["🐘 PostgreSQL<br/>Pessimistic Locking<br/>SELECT ... FOR UPDATE"]

    Worker["⚙️ Celery Worker<br/>10-Min Auto-Hold Expiration"]

    Client --> API
    API --> Redis
    API --> DB
    DB --> Worker
```

---

## ✨ Key System Features & Engineering Design

### 1. 🔒 Concurrency Strategy & Zero Double-Bookings
* **Pessimistic Database Locking**: Utilizes SQLAlchemy's `with_for_update()` to enforce row-level locking (`FOR UPDATE`) on PostgreSQL seat records during reservation transactions.
* **Race Condition Prevention**: Serializes concurrent requests attempting to claim the exact same seat, ensuring only **one transaction** succeeds while subsequent conflicting requests are safely rejected with `409 Conflict`.

### 2. 🚦 Upfront Traffic Shaping (Redis Queue)
* **Virtual Waiting Room**: Implements Redis Sorted Sets (`ZADD`/`ZRANK`) to throttle high-volume traffic spikes before they hit the core relational database.
* **Connection Pool Shielding**: Assigns dynamic queue tokens and position rankings, preventing database connection pool exhaustion during flash-sale events.

### 3. ⏳ Asynchronous Task Lifecycle & Auto-Expiration
* **Celery + Redis Broker**: Spawns background tasks with ETA triggers to manage temporary 10-minute seat holds.
* **Automatic Rollbacks**: If a user fails to complete payment within the hold window, Celery automatically releases the seat back to `AVAILABLE` status and marks the reservation as `EXPIRED`.

### 4. 🚀 High-Performance Async Operations & Schema Safety
* Built with asynchronous FastAPI endpoints and strict **Pydantic v2** data validation/serialization schemas.
* Modular database ORM separation using SQLAlchemy with custom field validators for relational mapping.

---

## 🛠️ Tech Stack

* **Framework**: FastAPI (Python 3.11+)
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **In-Memory Cache / Broker**: Redis
* **Task Queue**: Celery
* **Containerization**: Docker & Docker Compose
* **Benchmarking & Testing**: `asyncio` & `httpx`

---

## 🚦 Getting Started (Local Setup)

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* Python 3.11+ installed.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/movie-reservation-backend.git](https://github.com/your-username/movie-reservation-backend.git)
cd movie-reservation-backend

# 🚀 Setup & Run Guide

## 1. Set Up Virtual Environment

Create and activate a Python virtual environment.

### Create the Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Configure Environment Variables

Create a `.env` file in the project root and add the following:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/movie_db
REDIS_URL=redis://localhost:6379/0
```

---

## 3. Start Infrastructure (PostgreSQL & Redis)

Start the required services using Docker Compose.

```bash
docker compose up -d
```

---

## 4. Run the FastAPI Application

Start the API server:

```bash
python run.py
```

Once the server is running, the Swagger API documentation will be available at:

**http://127.0.0.1:8000/docs**

---

## 5. Start the Celery Worker

Open a **second terminal**, activate the virtual environment, and run the appropriate command for your operating system.

### Windows

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info -P solo
```

### macOS / Linux

```bash
celery -A app.workers.celery_app:celery_app worker --loglevel=info
```

---

# 🧪 Stress Testing & Concurrency Benchmarking

To verify database integrity under heavy concurrent requests, run the included stress test.

The script sends multiple asynchronous HTTP requests that attempt to reserve the **same seat row simultaneously**, ensuring that the booking system correctly handles race conditions.

Run:

```bash
python stress_test.py
```

## Expected Benchmark Results

```
Successful Bookings: 1

Rejected Conflicting Requests: N - 1 (HTTP 409 Conflict)

Double Bookings: 0
```

### ✅ Expected Behavior

- Exactly **one** booking succeeds.
- All conflicting requests are rejected with **HTTP 409 Conflict**.
- **Zero** double bookings should occur, demonstrating proper concurrency control and transactional integrity.