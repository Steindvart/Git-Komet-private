.PHONY: help install-backend install-frontend install init-db run-backend run-frontend test-backend test-frontend clean docker-up docker-down

help:
	@echo "Git-Komet - Team Effectiveness Analysis System"
	@echo ""
	@echo "Available commands:"
	@echo "  make install-backend    - Install backend dependencies"
	@echo "  make install-frontend   - Install frontend dependencies"
	@echo "  make install           - Install all dependencies"
	@echo "  make init-db           - Initialize database"
	@echo "  make run-backend       - Run backend server"
	@echo "  make run-frontend      - Run frontend server"
	@echo "  make test-backend      - Run backend tests"
	@echo "  make test-frontend     - Run frontend tests"
	@echo "  make docker-up         - Start with Docker Compose"
	@echo "  make docker-down       - Stop Docker Compose"
	@echo "  make clean             - Clean temporary files"
	@echo ""

install-backend:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && \
		(. venv/bin/activate || venv/Scripts/activate) && \
		pip install -r requirements.txt

install-frontend:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

install: install-backend install-frontend
	@echo "All dependencies installed!"

init-db:
	@echo "Initializing database..."
	cd backend && \
		(. venv/bin/activate || venv/Scripts/activate) && \
		python init_db.py

run-backend:
	@echo "Starting backend server..."
	cd backend && \
		(. venv/bin/activate || venv/Scripts/activate) && \
		python run.py

run-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm run dev

test-backend:
	@echo "Running backend tests..."
	cd backend && \
		(. venv/bin/activate || venv/Scripts/activate) && \
		pip install -r requirements-dev.txt && \
		pytest

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm run test

docker-up:
	@echo "Starting with Docker Compose..."
	docker-compose up --build

docker-down:
	@echo "Stopping Docker Compose..."
	docker-compose down

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.db" -delete 2>/dev/null || true
	rm -rf backend/.coverage 2>/dev/null || true
	rm -rf frontend/.nuxt 2>/dev/null || true
	rm -rf frontend/.output 2>/dev/null || true
	@echo "Clean complete!"
