# Flask Todo App Development Makefile

.PHONY: help install dev init-db reset-db seed-db test lint clean health stats setup

# Python and pip commands
PYTHON = python3
PIP = pip3
FLASK = flask

# Colors for output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "Flask Todo App Development Commands"
	@echo "=================================="
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Setup
install: ## Install Python dependencies
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	$(PIP) install -r requirements.txt

setup: install init-db seed-db ## Full development setup
	@echo "$(GREEN)Full development setup complete!$(NC)"

##@ Database
init-db: ## Initialize the database
	@echo "$(GREEN)Initializing database...$(NC)"
	$(PYTHON) scripts/dev_helpers.py init-db

reset-db: ## Reset the database (drop and recreate)
	@echo "$(YELLOW)Resetting database...$(NC)"
	$(PYTHON) scripts/dev_helpers.py reset-db

seed-db: ## Seed database with sample data
	@echo "$(GREEN)Seeding database...$(NC)"
	$(PYTHON) scripts/dev_helpers.py seed-db

stats: ## Show database statistics  
	@echo "$(GREEN)Database statistics:$(NC)"
	$(PYTHON) scripts/dev_helpers.py stats

##@ Development
dev: ## Run development server
	@echo "$(GREEN)Starting development server...$(NC)"
	$(PYTHON) run.py

dev-helper: ## Run development server with helper script
	@echo "$(GREEN)Starting development server with helper...$(NC)"
	$(PYTHON) scripts/dev_helpers.py dev-server

##@ Testing
test: ## Run tests
	@echo "$(GREEN)Running tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-coverage: ## Run tests with coverage
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=app --cov-report=html --cov-report=term

health: ## Check API health
	@echo "$(GREEN)Checking API health...$(NC)"
	$(PYTHON) scripts/dev_helpers.py health

test-api: ## Test API endpoints
	@echo "$(GREEN)Testing API endpoints...$(NC)"
	$(PYTHON) scripts/dev_helpers.py test-api

##@ Code Quality
lint: ## Run linting
	@echo "$(GREEN)Running linting...$(NC)"
	flake8 app/ --max-line-length=88 --extend-ignore=E203,W503

format: ## Format code with black
	@echo "$(GREEN)Formatting code...$(NC)"
	black app/ tests/ scripts/ --line-length=88

##@ Cleanup
clean: ## Clean up temporary files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

clean-db: ## Remove database files
	@echo "$(RED)Removing database files...$(NC)"
	rm -f instance/*.db

##@ Docker (if needed)
docker-build: ## Build Docker image
	@echo "$(GREEN)Building Docker image...$(NC)"
	docker build -t todo-backend .

docker-run: ## Run Docker container
	@echo "$(GREEN)Running Docker container...$(NC)"
	docker run -p 5000:5000 -e FLASK_ENV=development todo-backend

##@ Utilities
shell: ## Open Flask shell
	@echo "$(GREEN)Opening Flask shell...$(NC)"
	$(PYTHON) -c "from app import create_app, db; app = create_app(); app.app_context().push(); print('Flask shell ready! Available: app, db')"

logs: ## Show recent logs (if using a log file)
	@echo "$(GREEN)Recent logs:$(NC)"
	tail -f logs/app.log 2>/dev/null || echo "No log file found"

env-check: ## Check environment variables
	@echo "$(GREEN)Environment variables:$(NC)"
	@echo "FLASK_ENV: $${FLASK_ENV:-not set}"
	@echo "DATABASE_URL: $${DATABASE_URL:-not set}"
	@echo "SECRET_KEY: $${SECRET_KEY:+set}"