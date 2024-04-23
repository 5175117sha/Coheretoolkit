dev:
	@docker compose watch
test:
	docker compose run --build backend poetry run pytest src/backend/tests/$(file)
attach: 
	@docker attach cohere-toolkit-backend-1
exec-backend:
	docker exec -ti cohere-toolkit-backend-1 bash 
exec-db:
	docker exec -ti cohere-toolkit-db-1 bash
migration:
	docker compose run --build backend alembic -c src/backend/alembic.ini revision --autogenerate
migrate:
	docker compose run --build backend alembic -c src/backend/alembic.ini upgrade head
reset-db:
	docker compose down
	docker volume rm cohere_toolkit_db
setup:
	pip3 install -r cli/requirements.txt
	python3 cli/main.py
lint:
	poetry run black .
	poetry run isort . --show-files
first-run:
	make setup
	make migrate
	make dev
