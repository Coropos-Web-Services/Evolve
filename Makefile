.PHONY: help start stop restart logs build clean test install-server install-agent

help:
	@echo "EchoDesk Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install-server    Install server dependencies locally"
	@echo "  make install-agent     Install agent dependencies locally"
	@echo ""
	@echo "Docker:"
	@echo "  make start            Start all services"
	@echo "  make stop             Stop all services"
	@echo "  make restart          Restart all services"
	@echo "  make logs             View server logs"
	@echo "  make build            Rebuild containers"
	@echo ""
	@echo "Development:"
	@echo "  make dev-server       Run server locally (no Docker)"
	@echo "  make dev-agent        Run agent locally"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove containers and volumes"
	@echo "  make clean-db         Reset database"

# Docker commands
start:
	docker-compose up -d
	@echo "Server started at http://localhost:8000"
	@echo "API docs at http://localhost:8000/api/docs"

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f server

build:
	docker-compose build

clean:
	docker-compose down -v
	rm -rf data/*.db

clean-db:
	rm -rf data/*.db
	docker-compose restart server

# Local development
install-server:
	cd server && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -e ".[dev]"

install-agent:
	cd agent && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install -e ".[docker,dev]"

dev-server:
	cd server && \
	. venv/bin/activate && \
	uvicorn app.main:app --reload --port 8000

dev-agent:
	cd agent && \
	. venv/bin/activate && \
	python -m echodesk_agent

# Testing
test:
	cd server && . venv/bin/activate && pytest
	cd agent && . venv/bin/activate && pytest

# Quick setup
setup: build
	@echo "Creating .env file..."
	@if [ ! -f .env ]; then cp .env.example .env; fi
	@echo "Starting services..."
	@make start
	@echo ""
	@echo "✅ EchoDesk is ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Visit http://localhost:8000/api/docs"
	@echo "  2. Run 'make install-agent' to set up an agent"
	@echo "  3. Run 'make dev-agent' to start the agent"
