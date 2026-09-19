# auditflow — pilotage. Matrice serveur x base de données.
.DEFAULT_GOAL := help
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
DB_ENGINE ?= sqlite

help: ## Affiche cette aide
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	  awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-18s\033[0m %s\n",$$1,$$2}'

venv: ## Crée le venv et installe les dépendances
	python3 -m venv $(VENV)
	$(PIP) install -U pip
	$(PIP) install -r requirements-dev.txt

migrate: ## Applique les migrations (DB_ENGINE=sqlite|mysql|postgres)
	DB_ENGINE=$(DB_ENGINE) $(PY) manage.py migrate

seed: ## Charge les données de démonstration
	DB_ENGINE=$(DB_ENGINE) $(PY) manage.py seed_demo

check: ## Vérifie le projet
	DB_ENGINE=$(DB_ENGINE) $(PY) manage.py check

run-gunicorn: ## Lance sous gunicorn (port 8000)
	DB_ENGINE=$(DB_ENGINE) $(VENV)/bin/gunicorn config.wsgi:application \
	  -c deploy/gunicorn.conf.py

run-runserver: ## Lance le serveur de développement
	DB_ENGINE=$(DB_ENGINE) $(PY) manage.py runserver 0.0.0.0:8000

fakecdn: ## Lance le faux CDN instrumenté (port 9000) — voir tools/
	$(PY) tools/fake_cdn.py

audit: ## Lance pip-audit + bandit
	-$(VENV)/bin/pip-audit -r requirements.txt
	-$(VENV)/bin/bandit -q -r . -x $(VENV),tools

.PHONY: help venv migrate seed check run-gunicorn run-runserver fakecdn audit
