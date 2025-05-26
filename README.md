# Name Origin API

A solution to the Python Tech Task - A modern, domain-driven design (DDD) implementation of a name origin analysis API. This service provides insights into the probable origins of names based on statistical analysis and country data.

## 🎯 Task Overview

This project implements a service that predicts a person's likely country of origin based on their name and enriches it with additional country information. It integrates with two external APIs:
- [Nationalize.io](https://api.nationalize.io/) - for nationality prediction
- [REST Countries](https://restcountries.com/) - for country data enrichment

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
- **Docker**: Containerization with separate configurations for development and production
  - Development container includes testing and development libraries
  - Production container contains only necessary production dependencies
- **GitHub Actions**: CI/CD pipeline
- **uv 0.6.7**: Fast Python package installer and resolver

## 🚀 Getting Started

### Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose (for containerized setup)
- Git
- GNU Make

### Environment Variables

The project includes example environment files with all required variables:

1. For development:
   ```bash
   cp .env.example .env
   ```

2. For production:
   ```bash
   cp .env.prod.example .env.prod
   ```

All necessary environment variables are pre-configured in these example files.

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

### Development

The project uses Make commands for common development tasks:

1. Start all services (development):
   ```bash
   make all
   ```

2. Start only the application (development):
   ```bash
   make app
   ```

3. Start only the storage services:
   ```bash
   make storages
   ```

4. Run tests:
   ```bash
   make test
   ```

5. Run database migrations:
   ```bash
   make migrations
   ```

6. View application logs:
   ```bash
   make app-logs
   ```

7. Access application shell:
   ```bash
   make app-shell
   ```

8. Stop all services:
   ```bash
   make all-down
   ```

For production deployment, use the corresponding `-prod` commands:
```bash
make all-prod
make app-prod
make migrations-prod
make all-prod-down
```

The project supports two Docker container configurations:
- **Development**: Includes all development and testing tools, suitable for local development
- **Production**: Contains only necessary production dependencies, optimized for deployment

## 📚 API Documentation

Once the server is running, access the API documentation at:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### Available Endpoints

1. **GET /names/?name={name}**
   - Returns information about the most likely countries associated with a given name
   - Integrates with Nationalize.io and REST Countries APIs

2. **GET /popular-names/?country={country_code}**
   - Returns the top 5 most frequent names associated with a country
   - Uses country code (e.g., "US", "UA")

## 🔄 CI/CD Pipeline

The project uses GitHub Actions for continuous integration:

1. **Validate**: Runs pre-commit hooks and code formatting
2. **Test**: Executes the test suite

## 🧪 Testing

The project includes comprehensive tests:

- Unit tests for domain logic
- Integration tests for repositories
- API endpoint tests
- End-to-end tests

Run tests with:
```bash
make test
```

## 📝 Code Style

The project follows strict code style guidelines:

- Ruff for linting and formatting
- isort for import sorting
- mypy for type checking

Pre-commit hooks ensure code quality before commits.

## 🛠 Improvements & Technical Decisions

### Domain-Driven Design
- Implemented clean architecture with clear separation of concerns
- Used value objects for domain concepts
- Applied repository pattern for data access
- Implemented unit of work pattern for transaction management

### Performance Optimizations
- Implemented async/await for external API calls to improve response times
- Optimized database queries with proper indexing for faster data retrieval
- Implemented connection pooling to efficiently manage database connections
- Pre-fetching all countries in the first request since the operation is time-consuming, and with only around 250 countries, we can store them all efficiently

### Security Measures
- Implemented input validation using Pydantic models to ensure data integrity
- Secured environment variable handling to protect sensitive configuration
- Managed API keys for external services securely

### Potential Trade-offs
- Increased complexity due to DDD architecture
- Additional development time required for proper domain modeling
- More boilerplate code compared to simpler architectures
- Steeper learning curve for new developers
- Capital could be implemented as a foreign key in the future, but it's not necessary for the current requirements
- Border countries could be normalized into a separate table, which would increase complexity but only result in a maximum of 2500 rows (compared to 250), which is manageable for this system

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Bashar Hasan - [Abstract-333](https://github.com/Abstract-333)
