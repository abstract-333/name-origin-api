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
- **Testing**: Comprehensive test suite with pytest
- **CI**: GitHub Actions workflow for continuous integration (testing & Formating).
- **Code Quality**: Pre-commit hooks and linting tools

## ⚡ Quick Start

To start using the application, you only need:
1. Docker and Docker Compose installed
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/name-origin-api.git
   cd name-origin-api
   ```
3. Copy the environment files:
   ```bash
   cp .env.example .env
   cp .env.prod.example .env.prod
   ```
4. Start the application using either:

   With Make:
   ```bash
   make all
   make migrations
   ```

   Or directly with Docker Compose:
   ```bash
   # Start the application
   docker compose --profile dev -f docker_compose/storages.yaml -f docker_compose/app.yaml --env-file .env up --build -d
   
   # Run migrations
   docker exec -t main-app alembic upgrade head
   ```

5. Start exploring the API at:
   - Swagger UI: `http://localhost:8000/api/docs`
   - ReDoc: `http://localhost:8000/api/redoc`

That's it! You're ready to use the application.
> [!NOTE]
> You can run 
`make init-countries`
> after applying migrations that will fetch all countries from api, in order to achieve better optimization

## 🏗️ Architecture

The project follows Domain-Driven Design principles with a clean architecture:

```
.github/            # Github actions
app/
├── alembic/        # Alembic, for sql migrations
├── application/    # Application layer (API endpoints, schemas)
├── domain/         # Domain layer (entities, value objects)
├── infra/          # Infrastructure layer (repositories, models)
├── logic/          # Business logic layer (commands, handlers)
├── scripts/        # Python scripts
├── scripts/        # Settings, include the configuration of the system
└── tests/          # Test suite
```

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
- **GitHub Actions**: CI pipeline
- **uv 0.6.7**: Fast Python package installer and resolver

## 🚀 Getting Started
### Prerequisites

- Python 3.13 or higher
- Docker and Docker Compose (for containerized setup)
- Git
- GNU Make


### Make Commands Reference

The project uses Make commands to simplify common development and deployment tasks. Here's a comprehensive list of available commands:

#### Development Commands
- `make all` - Starts all services in development mode
- `make app` - Starts only the application in development mode
- `make storages` - Starts only the storage services (database, etc.)
- `make test` - Runs the test suite
- `make migrations` - Runs database migrations
- `make app-logs` - Shows application logs in real-time
- `make app-shell` - Opens a shell inside the application container
- `make all-down` - Stops all development services

#### Production Commands
- `make all-prod` - Starts all services in production mode
- `make app-prod` - Starts only the application in production mode
- `make storages-prod` - Starts storage services in production mode
- `make migrations-prod` - Runs database migrations in production
- `make all-prod-down` - Stops all production services

#### Database Management
- `make downgrade` - Rolls back the last migration
- `make downgrade-prod` - Rolls back the last migration in production
- `make create-migration` - Creates a new migration file
- `make create-migration-prod` - Creates a new migration file in production
- `make migrations-and-init` - Runs migrations and initializes the container
- `make init-countries` - Initializes country data in development
- `make init-countries-prod` - Initializes country data in production

The Make commands use Docker Compose profiles (`dev` and `prod`) to manage different environments and configurations. Each command is designed to work with the appropriate environment variables and Docker Compose files.

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

## 🔄 CI Pipeline——Without CD ):

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
- Pre-fetching all countries in the first request since the operation is time-consuming, and with only around 250 countries, we can store them all efficiently

### Security Measures
- Implemented input validation using Pydantic and dataclasses schemas to ensure data integrity
- Secured environment variable handling to protect sensitive configuration

### Potential Trade-offs
- Additional development time required for proper domain modeling
- More boilerplate code compared to simpler architectures

### Possible Improvements
- Capital could be implemented as a foreign key in the future, but it's not necessary for the current requirements
- Border countries could be normalized into a separate table, which would increase complexity but only result in a maximum of 2500 rows (compared to 250), which is manageable for this system
- Add caching (Redis, Memcached, ...)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Bashar Hasan - [Abstract-333](https://github.com/Abstract-333)
