include .env

.PHONY: up down logs ps api db

up:
	docker compose --env-file .env up -d --build

logs:
	docker compose logs -f --tail=200

down:
	docker compose down -v

ps:
	docker compose ps

api:
	@echo "API: http://localhost:$(API_PORT)/docs"

db:
	docker exec -it $$(docker ps -qf name=_db_1) psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)
