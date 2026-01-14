# Variables
PYTHON = python
PIP = pip
DOCKER_COMPOSE_FILE = docker-compose.yml

.PHONY: help install-backend setup-frontend ingest run-backend run-frontend up down clean clean-db clean-docker

help:
	@echo "BrandGuardian | Vaisala AI Assistant"
	@echo "-----------------------------------"
	@echo "  make install-backend   - Install Python dependencies"
	@echo "  make setup-frontend    - Install Node dependencies (requires npm)"
	@echo "  make ingest            - Run vector ingestion (requires backend .env)"
	@echo "  make up                - Start Full Stack (Backend + Frontend) in Docker"
	@echo "  make down              - Stop Docker containers"
	@echo "  make clean-db          - Reset Vector DB"

install-backend:
	cd backend && $(PIP) install -r requirements.txt

setup-frontend:
	cd frontend && npm install

ingest:
	cd backend && $(PYTHON) -m src.services.ingestion

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