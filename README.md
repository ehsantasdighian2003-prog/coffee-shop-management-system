# ☕ Coffee Shop Management System

A production-ready backend system for managing coffee shop operations, built with **FastAPI**, **PostgreSQL**, and a clean layered architecture.

This project provides a scalable API for managing users, products, categories, and orders with authentication, authorization, transaction management, and enterprise-level backend practices.

---

## 🚀 Version

Current Release:

```
v1.0.0
```

---

# ✨ Features

## 🔐 Authentication & Authorization

* JWT-based authentication
* Secure password hashing using Argon2
* Protected API routes
* Role-Based Access Control (RBAC)
* Admin/User permission management

---

## 👤 User Management

Implemented user management system including:

* User registration
* User authentication
* User profile management
* User activation/deactivation
* Role management
* Soft delete support
* Password update
* Account security fields

Supported user fields:

* Username
* Email
* First name
* Last name
* Phone number
* Role
* Active status
* Account timestamps

---

## ☕ Product Management

Complete product management module:

* Create products
* Update products
* Delete products
* Retrieve products
* Stock management
* Product activation status
* Category relationship

Advanced features:

* Pagination
* Search
* Filtering
* Sorting
* Metadata responses

---

## 🗂 Category Management

Category module includes:

* Category CRUD operations
* Product-category relationship
* Category based filtering

---

## 🛒 Order Management

Complete order workflow:

* Create orders
* Retrieve orders
* Update orders
* Delete orders
* Order items management
* Automatic stock handling
* Transaction-safe operations

Advanced order features:

* Pagination
* Search
* Filtering
* Sorting
* Total calculation

---

# 🛠 Tech Stack

## Backend

* Python 3.13
* FastAPI
* Pydantic v2
* Uvicorn

## Database

* PostgreSQL
* psycopg2

## Security

* JWT Authentication
* Argon2 Password Hashing
* Role Based Access Control

## Development Tools

* Swagger / OpenAPI Documentation
* Git
* VS Code

---

# 🏗 Architecture

The project follows a layered architecture:

```
                API Request

                    ↓

              Router Layer

                    ↓

             Service Layer

                    ↓

           Repository Layer

                    ↓

          PostgreSQL Database
```

---

## Architectural Principles

* Separation of concerns
* Dependency injection
* Repository Pattern
* Service Layer Pattern
* Transaction management
* Clean code principles

---

# 🔄 Unit Of Work Pattern

Database transactions are managed using UnitOfWork.

Benefits:

* Centralized transaction handling
* Commit/Rollback management
* Consistent repository lifecycle
* Safer database operations

Example flow:

```
Request
   |
Service
   |
UnitOfWork
   |
Repository
   |
Database
```

---

# 📂 Project Structure

```
coffee-shop-management-system/

│
├── app/
│   │
│   ├── core/
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── unit_of_work.py
│   │   └── exceptions.py
│   │
│   ├── routes/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   └── orders.py
│   │
│   ├── services/
│   │
│   ├── repositories/
│   │
│   ├── schemas/
│   │
│   └── main.py
│
├── alembic/
│
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/coffee-shop-management-system.git

cd coffee-shop-management-system
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file:

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/coffee_shop

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# 🗄 Database Setup

Create PostgreSQL database:

```
coffee_shop
```

Run migrations:

```bash
alembic upgrade head
```

---

# ▶️ Running The Application

Start server:

```bash
uvicorn app.main:app --reload
```

Application runs on:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```
http://127.0.0.1:8000/openapi.json
```

---

# 🔑 Authentication Flow

1. Register user

```
POST /auth/register
```

2. Login

```
POST /auth/login
```

3. Receive JWT token

4. Use token:

```
Authorization: Bearer <token>
```

5. Access protected endpoints

---

# 🧪 Quality & Testing

Completed:

* API endpoint testing
* Authentication testing
* Authorization testing
* CRUD validation
* Negative scenario testing
* Transaction testing

---

# 🗺 Roadmap

## Version 1.0.0 ✅

Completed:

* Authentication
* User Management
* Product Management
* Category Management
* Order Management
* Security
* Exception Handling
* Logging
* UnitOfWork
* API Documentation

---

## Version 1.1.0 🚧

Planned:

* Docker
* Docker Compose
* Automated Testing with Pytest
* CI/CD Pipeline

---

## Version 2.0.0 🚀

Future:

* React / Next.js Frontend
* Cloud Deployment
* Monitoring
* Advanced Analytics
* Notification System

---

# 🤝 Contribution

Contributions, suggestions, and improvements are welcome.

---

# 📄 License

This project is licensed under the MIT License.
