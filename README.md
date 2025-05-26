# Name Origin API

A modern, domain-driven design (DDD) implementation of a name origin analysis API. This service provides insights into the probable origins of names based on statistical analysis and country data.

## 🚀 Features

- **Name Origin Analysis**: Determine the probable country of origin for given names
- **Country Information**: Rich country data including flags, capitals, and geographical information
- **RESTful API**: FastAPI-based REST API with OpenAPI documentation
- **Domain-Driven Design**: Clean architecture with clear separation of concerns
- **Async Support**: Built with async/await for high performance
- **Type Safety**: Full type hints and static type checking
- **Testing**: Comprehensive test suite with pytest
- **CI/CD**: GitHub Actions workflow for continuous integration
- **Code Quality**: Pre-commit hooks and linting tools

## 🏗️ Architecture

The project follows Domain-Driven Design principles with a clean architecture:

```
app/
├── application/     # Application layer (API endpoints, schemas)
├── domain/         # Domain layer (entities, value objects)
├── infra/          # Infrastructure layer (repositories, models)
├── logic/          # Business logic layer (commands, handlers)
└── tests/          # Test suite
```

### Key Components

- **Domain Layer**: Contains core business entities and value objects
  - `CountryEntity`: Represents country data
  - `NameEntity`: Represents name analysis results
  - Value Objects: `Name`, `Probability`, `CountOfRequests`

- **Infrastructure Layer**: Implements data access and external services
  - SQLAlchemy models and repositories
  - External API integrations
  - Converters for model-entity transformations

- **Application Layer**: Handles HTTP requests and responses
  - FastAPI endpoints
  - Pydantic schemas
  - Error handling

- **Logic Layer**: Implements business rules
  - Command handlers
  - Domain services
  - Event handlers

## 🛠️ Technology Stack

- **Python 3.13+**: Modern Python features and type hints
- **FastAPI**: High-performance web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Alembic**: Database migrations
- **Pytest**: Testing framework
- **Ruff**: Fast Python linter
- **Pre-commit**: Git hooks for code quality
- **Docker**: Containerization
- **GitHub Actions**: CI/CD pipeline

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose (for containerized setup)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/name-origin-api.git
   cd name-origin-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

### Development

1. Install development dependencies:
   ```bash
   uv pip install -e ".[dev,test,lint]"
   ```

2. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run the development server:
   ```bash
   uvicorn application.main:app --reload
   ```

### Testing

Run the test suite:
```bash
pytest
```

### Docker

Build and run with Docker Compose:
```bash
docker-compose -f docker_compose/dev.yml up --build
```

## 📚 API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

1. **Validate**: Runs pre-commit hooks and code formatting
2. **Test**: Executes the test suite
3. **Build**: Creates Docker images
4. **Deploy**: Deploys to production (if configured)

## 🧪 Testing

The project includes comprehensive tests:

- Unit tests for domain logic
- Integration tests for repositories
- API endpoint tests
- End-to-end tests

Run tests with:
```bash
pytest
```

## 📝 Code Style

The project follows strict code style guidelines:

- Black for code formatting
- Ruff for linting
- isort for import sorting
- mypy for type checking

Pre-commit hooks ensure code quality before commits.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Bashar Hasan - [Abstract-333](https://github.com/Abstract-333)

## 🙏 Acknowledgments

- FastAPI community
- SQLAlchemy team
- All contributors and maintainers 