# Variables
PYTHON = python
PIP = pip
DOCKER_COMPOSE_FILE = docker-compose.yml

.PHONY: help install-backend setup-frontend ingest up down clean clean-db clean-docker test-backend test-frontend test-all clean

help:
	@echo "BrandGuardian | Vaisala AI Assistant"
	@echo "-----------------------------------"
	@echo "  make install-backend   - Install Python dependencies"
	@echo "  make setup-frontend    - Install Node dependencies"
	@echo "  make ingest            - Ingest data into the vector database"
	@echo "  make test-backend      - Run Python unit tests with coverage"
	@echo "  make test-frontend     - Run React component tests"
	@echo "  make test-all          - Run ALL tests"
	@echo "  make up                - Start Full Stack in Docker"

install-backend:
	cd backend && $(PIP) install -r requirements.txt && $(PIP) install pytest pytest-asyncio pytest-cov httpx

setup-frontend:
	cd frontend && npm install

ingest:
	cd backend && $(PYTHON) -m src.services.ingestion

# Testing Commands
test-backend:
	cd backend && pytest --cov=src tests/ -v

test-frontend:
	cd frontend && npm run test

test-all: test-backend test-frontend

# Development (Docker)
up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build
	@echo "BrandGuardian is running! Access the frontend at http://localhost:3000"

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

clean-db:
	rm -rf backend/data/chroma_db

clean-docker:
	docker system prune -f

clean:
	@echo "🧹 Cleaning Python bytecode, cache, and coverage files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	@echo "✅ Clean complete."