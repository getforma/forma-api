# Makefile for Forma API

# Variables
PYTHON = python3
FLASK = flask
PIP = pip

# Default target
all: install run

# Install dependencies
install:
	$(PIP) install -r requirements.txt

# Run the Flask application
run:
	$(PYTHON) -m flask run

# Run tests
test:
	$(PYTHON) -m pytest tests/ -p no:warnings

# Clean up pyc files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Phony targets
.PHONY: all install run test clean
