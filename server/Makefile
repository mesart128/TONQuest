lint-fix:
	@echo "Fixing issues with linter Ruff ..."
	@ruff format .
	@ruff check . --fix
	@echo "Linting is complete"

r:
	poetry run uvicorn main:app --host localhost --port 2024 --reload

rscan:
	sh deploy/entrypoints/run_scanner.sh

dupb:
	docker compose -f docker-compose_dev.yml up --build
ddown:
	docker compose -f docker-compose_dev.yml down

run_server:
	sh deploy/entrypoints/run_python.sh

migrate:
	alembic upgrade head