Mini CMS

A lightweight content management system (CMS) built with **FastAPI**, **SQLAlchemy**, and **Alembic**.  
The project is containerized with Docker and supports migrations, testing, and environment-based configuration.

---

## 🚀 Features
- Fast and modern backend powered by [FastAPI]
- Database migrations with [Alembic]
- Environment-based configuration using `.env` files  
- Docker and Docker Compose setup for local development and testing  
- Unit and integration tests with [pytest]
- RESTful API with automatic OpenAPI/Swagger documentation  

---

## 📂 Project Structure
Mini_cms/
│
├── app/ # Application source code
│ ├── routers/ # API routers (endpoints)
│ ├── models/ # SQLAlchemy models
│ ├── schemas/ # Pydantic schemas
│ ├── core/ # Config, dependencies, utils
│ └── main.py # FastAPI entry point
│
├── alembic/ # Database migrations
├── tests/ # Unit and integration tests
│
├── docker-compose.yml # Local development environment
├── Dockerfile # Application container
├── pyproject.toml # Poetry dependencies and project metadata
├── .env.example # Example environment variables
└── README.md

Run with Docker
Build and start the application with Docker Compose:
docker compose up --build

The application will be available at:
API (Swagger UI): http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

#alembic revision --autogenerate -m "all tables"

#docker compose run --rm api taskiq worker app.taskiq_broker:broker --fs-discover --tasks-pattern "**/tasks"    # запустить worker в контейнере
