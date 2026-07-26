# ☕ Coffee Shop Management System

<p align="center">
  <b>Production-ready Coffee Shop Management System Backend</b><br>
  Built with FastAPI, PostgreSQL and Enterprise-Level Backend Architecture
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Production-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Alembic](https://img.shields.io/badge/Migration-Alembic-red)
![Pytest](https://img.shields.io/badge/Testing-Pytest-success)

</p>

---

# 📌 Overview

Coffee Shop Management System is a production-oriented backend application designed to manage coffee shop operations including users, products, categories, and orders.

The project is built with modern backend engineering principles focusing on:

- Clean Architecture
- Scalability
- Maintainability
- Security
- Separation of Concerns
- Professional API Design

The goal of this project is to demonstrate how a real-world backend system can be designed using enterprise-level practices.

---

# 🚀 Key Features

## 🔐 Authentication & Security

- JWT Authentication
- Secure password hashing using Argon2
- Protected API endpoints
- Role-Based Access Control (RBAC)
- User authorization management


## 👥 User Management

- User registration
- User authentication
- Profile management
- Role management
- Account activation/deactivation
- Soft delete support


## ☕ Product Management

- Complete CRUD operations
- Product inventory management
- Price management
- Category relationship
- Search functionality
- Filtering
- Sorting
- Pagination


## 📂 Category Management

- Category CRUD operations
- Product-category relationships
- Category-based filtering


## 🛒 Order Management

- Create and manage orders
- Order items handling
- Automatic stock validation
- Database transactions
- Order history
- Pagination
- Filtering
- Sorting

---

# 🏗 Architecture

The project follows a layered architecture:

                Client
                  |
                  |
             FastAPI Routes
                  |
                  |
            Service Layer
                  |
                  |
          Repository Layer
                  |
                  |
          PostgreSQL Database


This architecture provides:

- Clear responsibility separation
- Easier testing
- Better maintainability
- Future scalability

---

# 🧩 Design Patterns

## Repository Pattern

Database operations are isolated inside repository classes.

Benefits:

- Cleaner business logic
- Easier database changes
- Better testability


## Service Layer Pattern

Business rules are handled inside services instead of API routes.


## Unit Of Work Pattern

Transaction management layer responsible for:

- Commit handling
- Rollback handling
- Repository coordination

---

# 🛠 Technology Stack

## Backend

- Python 3.13
- FastAPI
- Pydantic v2
- Uvicorn


## Database

- PostgreSQL
- psycopg2


## Security

- JWT
- python-jose
- Argon2


## Database Migration

- Alembic


## Testing

- Pytest
- Pytest Coverage

---

# 📂 Project Structure

coffee-shop-management-system

│
├── app
│
├── core
│ ├── database.py
│ ├── security.py
│ ├── exceptions.py
│ ├── handlers.py
│ └── unit_of_work.py
│
├── routes
│ ├── auth.py
│ ├── users.py
│ ├── products.py
│ ├── categories.py
│ └── orders.py
│
├── services
│ ├── user_service.py
│ ├── product_service.py
│ ├── category_service.py
│ └── order_service.py
│
├── repositories
│ ├── user_repository.py
│ ├── product_repository.py
│ ├── category_repository.py
│ └── order_repository.py
│
├── schemas
│
├── tests
│
├── migrations
│
└── main.py


---

# 📖 API Documentation

The project provides interactive API documentation using Swagger UI.

Available at:

http://localhost:8000/docs


Alternative documentation:

http://localhost:8000/redoc


---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/coffee-shop-management-system.git

Enter Project Directory
cd coffee-shop-management-system

Create Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
🔧 Environment Configuration

Create a .env file:

DATABASE_URL=postgresql://username:password@localhost:5432/coffee_shop

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
🗄 Database Setup

Run migrations:

alembic upgrade head
▶️ Running Application

Start development server:

uvicorn app.main:app --reload

Application will be available at:

http://localhost:8000
🧪 Testing

Run tests:

pytest

Run with coverage:

pytest --cov
📊 Current Status
Backend Progress
█████████░ 90%

Completed:

✅ Authentication System
✅ JWT Security
✅ User Management
✅ Product Management
✅ Category Management
✅ Order Management
✅ Repository Pattern
✅ Service Layer
✅ Unit Of Work
✅ Exception Handling
✅ Logging System
✅ API Documentation
✅ QA Testing

🚀 Roadmap
Version 1.0
 Backend Foundation
 Authentication
 User Management
 Product Management
 Category Management
 Order Management
 Database Migration
 Testing
Future Improvements
Docker Containerization
CI/CD Pipeline
Cloud Deployment
Monitoring System
Redis Caching
React / Next.js Frontend
Automated Deployment
💡 Project Goals

This project demonstrates:

Professional backend architecture
Secure API development
Database design
REST API engineering
Production-oriented coding practices
👨‍💻 Author

Backend Developer Portfolio Project

Built with ❤️ using:

FastAPI + PostgreSQL + Python


paste after:

```bash
git add README.md
git commit -m "docs: improve professional README"
git push