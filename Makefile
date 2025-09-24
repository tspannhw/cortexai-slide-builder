# Snowflake Cortex AI Slide Builder - Makefile
# Modern development workflow using UV package manager

.PHONY: help install test lint format type-check security clean build run docs deploy

# Default target
help: ## Show this help message
	@echo "Snowflake Cortex AI Slide Builder - Development Commands"
	@echo "======================================================="
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development setup
install: ## Install dependencies and setup development environment
	@echo "🚀 Setting up development environment..."
	@command -v uv >/dev/null 2>&1 || (echo "Installing UV..." && curl -LsSf https://astral.sh/uv/install.sh | sh)
	uv sync --extra dev --extra test --extra docs
	@echo "✅ Development environment ready!"

install-ci: ## Install dependencies for CI/CD
	uv sync --extra test

# Code quality
lint: ## Run linting checks
	@echo "🔍 Running linting checks..."
	uv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	uv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	uv run black .
	uv run isort .

format-check: ## Check code formatting without making changes
	@echo "🔍 Checking code formatting..."
	uv run black --check .
	uv run isort --check-only .

type-check: ## Run type checking with mypy
	@echo "🔬 Running type checks..."
	uv run mypy . --ignore-missing-imports

security: ## Run security checks
	@echo "🔒 Running security checks..."
	uv run bandit -r . -f json -o bandit-report.json || true
	uv run bandit -r . --skip B101,B601

quality: format-check lint type-check security ## Run all code quality checks

# Testing
test: ## Run all tests
	@echo "🧪 Running tests..."
	./scripts/test.sh

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	uv run pytest tests/ -m "unit" -v

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	uv run pytest tests/ -m "integration" -v

test-e2e: ## Run end-to-end tests
	@echo "🧪 Running end-to-end tests..."
	uv run pytest tests/ -m "e2e" -v

test-fast: ## Run fast tests (exclude slow tests)
	@echo "🧪 Running fast tests..."
	uv run pytest tests/ -m "not slow" -v

test-coverage: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	uv run pytest tests/ --cov=. --cov-report=html --cov-report=term --cov-report=xml

test-watch: ## Run tests in watch mode
	@echo "🧪 Running tests in watch mode..."
	uv run ptw -- tests/ -v

# Application
run: ## Run the application locally
	@echo "🚀 Starting Snowflake Cortex AI Slide Builder..."
	./scripts/run.sh

run-demo: ## Run the application in demo mode
	@echo "🎭 Starting application in demo mode..."
	./scripts/run.sh --demo

run-debug: ## Run the application with debug logging
	@echo "🐛 Starting application with debug logging..."
	./scripts/run.sh --debug

run-port: ## Run the application on custom port (make run-port PORT=8080)
	@echo "🚀 Starting application on port $(PORT)..."
	./scripts/run.sh --port $(PORT)

# Building
build: ## Build the package
	@echo "📦 Building package..."
	uv build

build-wheel: ## Build wheel distribution
	@echo "📦 Building wheel..."
	uv build --wheel

build-sdist: ## Build source distribution
	@echo "📦 Building source distribution..."
	uv build --sdist

# Documentation
docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	@mkdir -p docs/build
	@echo "Documentation available in docs/ directory"

docs-serve: ## Serve documentation locally
	@echo "📚 Serving documentation..."
	cd docs && python -m http.server 8000

docs-api: ## Generate API documentation
	@echo "📚 Generating API documentation..."
	uv run python -c "import pydoc; pydoc.writedoc('cortex_integration')"
	uv run python -c "import pydoc; pydoc.writedoc('real_cortex_app')"

# Deployment
deploy-check: ## Check deployment readiness
	@echo "🔍 Checking deployment readiness..."
	@command -v snowsql >/dev/null 2>&1 || (echo "❌ SnowSQL not found. Please install SnowSQL for Snowflake deployment." && exit 1)
	@test -f deploy_to_snowflake.sql || (echo "❌ Deployment script not found" && exit 1)
	@echo "✅ Deployment check passed"

deploy-local: ## Deploy for local development
	@echo "🚀 Setting up local deployment..."
	make install
	make test-fast
	@echo "✅ Local deployment ready"

deploy-staging: ## Deploy to staging environment
	@echo "🚀 Deploying to staging..."
	make quality
	make test
	make build
	@echo "✅ Staging deployment ready"

deploy-production: ## Deploy to production (requires manual confirmation)
	@echo "🚨 Production deployment requires manual confirmation"
	@read -p "Are you sure you want to deploy to production? [y/N] " confirm && [ "$$confirm" = "y" ]
	make quality
	make test
	make security
	make build
	@echo "✅ Production deployment ready"

# Database operations
db-check: ## Check Snowflake connection
	@echo "🔍 Checking Snowflake connection..."
	@command -v snowsql >/dev/null 2>&1 || (echo "❌ SnowSQL not found" && exit 1)
	snowsql -q "SELECT CURRENT_VERSION();" || echo "❌ Snowflake connection failed"

db-deploy: ## Deploy database objects to Snowflake
	@echo "🚀 Deploying to Snowflake..."
	snowsql -f deploy_to_snowflake.sql

db-status: ## Check Streamlit app status in Snowflake
	@echo "🔍 Checking Streamlit app status..."
	snowsql -q "SHOW STREAMLITS;"

# Maintenance
clean: ## Clean up build artifacts and cache
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

clean-all: clean ## Clean everything including virtual environment
	rm -rf .venv/
	rm -rf uv.lock

update: ## Update dependencies
	@echo "📦 Updating dependencies..."
	uv sync --upgrade

update-dev: ## Update development dependencies
	@echo "📦 Updating development dependencies..."
	uv sync --upgrade --extra dev --extra test --extra docs

# Utility targets
env: ## Show environment information
	@echo "Environment Information:"
	@echo "======================="
	@echo "Python: $(shell python --version 2>&1)"
	@echo "UV: $(shell uv --version 2>&1)"
	@echo "Platform: $(shell uname -s)"
	@echo "Working Directory: $(shell pwd)"
	@echo "Virtual Environment: $(VIRTUAL_ENV)"

requirements: ## Generate requirements.txt from pyproject.toml
	@echo "📝 Generating requirements.txt..."
	uv pip compile pyproject.toml -o requirements.txt

pre-commit: ## Run pre-commit checks
	@echo "🔍 Running pre-commit checks..."
	make format-check
	make lint
	make type-check
	make security
	make test-fast

ci: install-ci quality test ## Run CI pipeline
	@echo "🚀 CI pipeline completed successfully!"

# Docker targets (if using Docker)
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t cortex-slide-builder .

docker-run: ## Run Docker container
	@echo "🐳 Running Docker container..."
	docker run -p 8501:8501 cortex-slide-builder

docker-push: ## Push Docker image to registry
	@echo "🐳 Pushing Docker image..."
	docker push cortex-slide-builder

# Development helpers
dev-setup: install ## Complete development setup
	@echo "🛠️  Setting up development environment..."
	make install
	make test-fast
	@echo "✅ Development setup complete!"

dev-reset: clean-all install ## Reset development environment
	@echo "🔄 Resetting development environment..."

quick-check: format-check lint test-fast ## Quick development checks

# Release targets
release-patch: ## Create patch release
	@echo "🏷️  Creating patch release..."
	@echo "Bump version and create git tag manually"

release-minor: ## Create minor release  
	@echo "🏷️  Creating minor release..."
	@echo "Bump version and create git tag manually"

release-major: ## Create major release
	@echo "🏷️  Creating major release..."
	@echo "Bump version and create git tag manually"

# Help target (default)
.DEFAULT_GOAL := help
