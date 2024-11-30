# Makefile for Forma API

# Variables
PYTHON = python3
FLASK = flask
PIP = pip
PSQL = psql

# Database variables
DB_USER = forma
DB_PASSWORD = forma
DB_HOST = localhost
DB_NAME_DEV = forma_dev
DB_NAME_TEST = forma_test

# Default target
all: install run

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run the Flask application
run:
	$(PYTHON) -m flask run

# Create databases
create-dbs:
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "CREATE DATABASE $(DB_NAME_DEV);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "CREATE DATABASE $(DB_NAME_TEST);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $(DB_NAME_DEV) TO $(DB_USER);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE $(DB_NAME_TEST) TO $(DB_USER);"
	# Grant schema permissions for development database
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME_DEV) -c "GRANT ALL ON SCHEMA public TO $(DB_USER);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME_DEV) -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $(DB_USER);"
	# Grant schema permissions for test database
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME_TEST) -c "GRANT ALL ON SCHEMA public TO $(DB_USER);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d $(DB_NAME_TEST) -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $(DB_USER);"

# Drop databases
drop-dbs:
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "DROP DATABASE IF EXISTS $(DB_NAME_DEV);"
	PGPASSWORD=$(DB_PASSWORD) $(PSQL) -h $(DB_HOST) -U $(DB_USER) -d postgres -c "DROP DATABASE IF EXISTS $(DB_NAME_TEST);"

# Run migrations
migrate:
	$(FLASK) db upgrade

# Run tests with coverage
test:
	FLASK_ENV=test $(PYTHON) -m pytest tests/ -p no:warnings --cov=. --cov-report=xml --cov-report=term-missing:skip-covered

# Clean up pyc files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Reset everything and setup fresh
reset: drop-dbs create-dbs migrate

# Phony targets
.PHONY: all install run test clean create-dbs drop-dbs migrate reset
