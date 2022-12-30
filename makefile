## @ start
.PHONY: run down
run: ## run docker compose
	@docker compose -f docker-compose.dev.yaml up

down: ## stop docker compose
	@docker compose -f docker-compose.dev.yaml down

local: ## stop application in localhost without db
	@python manage.py runserver

## @ format
.PHONY: black isort format
isort:
	@pipenv run isort .
blue:
	@pipenv run blue . --extend-exclude 'database|.history'
format: isort blue ## perform formatting on all files with isort and blue

## @ requirements
.PHONY: requirements requirements_dev
requirements: ## generate requirements.txt only production extensions
	@pipenv requirements > requirements.txt

requirements_dev: ## generate requirements.txt with development extensions
	@pipenv requirements --dev > requirements.dev.txt

help:
	@pipenv run python help.py