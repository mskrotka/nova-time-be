env:
	cp .env_example .env

up:
	docker compose -f docker-compose.dev.yaml up -d

stop:
	docker compose -f docker-compose.dev.yaml stop

build:
	docker compose -f docker-compose.dev.yaml up -d --force-recreate --build

up-prod:
	docker compose -f docker-compose.prod.yaml up -d

stop-prod:
	docker compose -f docker-compose.prod.yaml stop

build-prod:
	docker compose -f docker-compose.prod.yaml up -d --force-recreate --build

fix:
	docker exec -it novatime-app python manage.py loaddata core/fixtures/admin_user.json

migrate:
	docker exec -it novatime-app python manage.py migrate

migrations:
	docker exec -it novatime-app python manage.py makemigrations

app_shell:
	docker exec -it novatime-app bash

shell_plus:
	docker exec -it novatime-app python manage.py shell

test:
	docker exec -it novatime-app python manage.py test

clean-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

startapp:
	docker exec -it novatime-app python manage.py startapp $(name)

logs:
	docker logs -f $(container)
