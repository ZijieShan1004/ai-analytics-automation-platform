.PHONY: up down build logs restart ps migrate revision test-backend test-ml test-all format-backend shell-api shell-worker shell-db clean

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

restart:
	docker compose down
	docker compose up --build

ps:
	docker compose ps

migrate:
	docker compose exec api sh -c "cd /app/backend && alembic upgrade head"

revision:
	docker compose exec api sh -c "cd /app/backend && alembic revision --autogenerate -m \"$(message)\""

test-backend:
	docker compose exec api sh -c "cd /app/backend && pytest -q"

test-ml:
	docker compose exec api sh -c "cd /app/ml && pytest -q"

test-all:
	docker compose exec api sh -c "cd /app/backend && pytest -q"
	docker compose exec api sh -c "cd /app/ml && pytest -q"

format-backend:
	docker compose exec api sh -c "cd /app/backend && ruff format app tests"

shell-api:
	docker compose exec api sh

shell-worker:
	docker compose exec worker sh

shell-db:
	docker compose exec postgres psql -U postgres -d analytics_platform

clean:
	docker compose down -v