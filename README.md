# Name Origin Service

A service that predicts a person's likely country of origin based on their name and enriches it with additional country information.

## 🚀 Features

- Predict nationality based on names using Nationalize.io API
- Enrich country data using REST Countries API
- JWT Authentication
- OpenAPI Documentation (Swagger/ReDoc)
- Docker containerization
- Unit tests with pytest

## 🛠 Technical Stack

- FastAPI
- SQLAlchemy
- Alembic for migrations
- PostgreSQL
- Docker & Docker Compose
- Domain-Driven Design (DDD) architecture
- Pydantic for data validation
- Ruff for linting and formatting

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Poetry for dependency management

## 🔧 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/name_origin_db

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys (if needed)
NATIONALIZE_API_KEY=your-nationalize-api-key
```

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd name-origin-service
```

2. Install dependencies:
```bash
poetry install
```

3. Start the services using Docker Compose:
```bash
docker-compose up -d
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Running Tests

```bash
pytest
```

## 🛠 Improvements & Technical Decisions

### Domain-Driven Design Implementation
- Clear separation of concerns with domain, application, and infrastructure layers
- Rich domain models with encapsulated business logic
- Repository pattern for data access abstraction

### Performance Optimizations
- Caching of API responses to reduce external API calls
- Database indexing for frequently queried fields
- Connection pooling for database operations

### Security Measures
- JWT-based authentication
- Input validation using Pydantic models
- Rate limiting for API endpoints
- Secure password hashing

### Potential Trade-offs
- Increased complexity due to DDD architecture
- Additional development time for proper domain modeling
- More boilerplate code compared to simpler architectures

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 