# Finance Dashboard Backend API

This project is a backend system for a finance dashboard application. It is built using FastAPI and demonstrates backend concepts such as API design, data modeling, access control, and data processing.

The system allows different types of users to interact with financial records based on their roles and provides summary insights for dashboard visualization.

## Overview

The backend supports:

- User management with role-based permissions
- CRUD operations for financial records
- Filtering and querying of transaction data
- Dashboard APIs for aggregated insights
- Authentication using JWT tokens
- Input validation and structured error handling
- Database persistence using SQLAlchemy

The focus of this project is on clean backend structure, logical separation of concerns, and correct handling of data and access control.

## Features Implemented

- User and Role Management
- Financial Records CRUD
- Record Filtering (by date, category, type)
- Dashboard Summary APIs (totals, trends)
- Role Based Access Control
- Input Validation and Error Handling
- Data Persistence using a relational database

## Technology Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** PostgreSQL (with SQLite used for testing)
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** bcrypt via passlib
- **Testing:** pytest

## Project Structure

```bash
app/
    api/            # API routes and dependencies
    core/           # configuration and security logic
    db/             # database setup and base models
    models/         # database models
    schemas/        # request/response validation schemas
    services/       # business logic layer
    main.py         # application entry point

tests/
    test_api/       # endpoint tests
    conftest.py     # test configuration and fixtures

alembic/            # database migrations
seed.py             # script to create initial admin user
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Finance_Data_Processing_and_Access_Control_Backend
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` and provide values such as:

- Database URL
- Secret key
- Token expiry

### 5. Start the database (if using Docker)

```bash
docker-compose up -d
```

### 6. Run migrations

```bash
alembic upgrade head
```

### 7. Seed initial admin user

```bash
python seed.py
```

**Default credentials:**

- Email: `admin@example.com`
- Password: `admin123`

### 8. Run the server

```bash
python -m uvicorn app.main:app --reload
```

API documentation will be available at:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Overview

### Authentication

- **POST** `/api/v1/auth/login`  
  Returns a JWT token for authenticated access

### Users (Admin only)

- `GET /api/v1/users/`
- `POST /api/v1/users/`
- `PUT /api/v1/users/{id}`
- `DELETE /api/v1/users/{id}`

### Transactions

- `GET /api/v1/transactions/`  
  Supports filtering by type, category, and date range
- `POST /api/v1/transactions/`
- `GET /api/v1/transactions/{id}`
- `PUT /api/v1/transactions/{id}`
- `DELETE /api/v1/transactions/{id}`

### Dashboard

- `GET /api/v1/dashboard/summary`  
  Returns total income, expenses, balance, and recent activity
- `GET /api/v1/dashboard/trends`  
  Returns grouped data (monthly or weekly)

## Access Control

The system defines three roles:

- **Viewer** – Can access dashboard data only
- **Analyst** – Can view transactions and dashboard insights
- **Admin** – Full access to users and transactions

Access is enforced at the backend using dependency-based checks.

## Testing

Tests are written using `pytest`. To run tests:

```bash
pytest tests/ -v
```

Tests use an isolated SQLite database to avoid affecting development data.

## Assumptions

- Transactions are soft deleted instead of permanently removed
- Roles define clear boundaries for allowed actions
- Dashboard data is computed only from active (non-deleted) records
- SQLite is used for testing, while PostgreSQL is used for development
