## @ start
.PHONY: up down
up: ## run docker compose
	@docker compose -f docker-compose.dev.yaml up

down: ## stop docker compose
	@docker compose -f docker-compose.dev.yaml down

local: ## stop application in localhost without db
	@python manage.py runserver

mail:
	@docker run -p 8025:8025 -p 1025:1025 mailhog/mailhog

## @ format
.PHONY: black isort format
isort:
	@pipenv run isort --gitignore .
blue:
	@pipenv run blue .
format: isort blue ## perform formatting on all files with isort and blue

## @ tests
.PHONY: test testm testr test_c test_s test_c_s
test: ## run tests without migrations
	@pipenv run pytest --nomigrations -s apps

test_m: ## run tests with migrations
	@pipenv run pytest -s apps

test_c: ## run tests with migrations and generate coverage html
	@pipenv run pytest -s --cov-report html --cov=apps

test_s: ## run http server in localhost:9000 with coverage results
	@pipenv run python -m http.server 9000 --directory htmlcov

test_c_s: test_c test_s ## run tests with coverage and run http server in localhost:9000 with results

## @ requirements
.PHONY: requirements requirements_dev
requirements: ## generate requirements.txt only production extensions
	@pipenv requirements > requirements.txt

requirements_dev: ## generate requirements.txt with development extensions
	@pipenv requirements --dev > requirements.dev.txt

help:
	@pipenv run python help.py