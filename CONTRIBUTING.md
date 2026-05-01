# Contributing to the ESG Grid Oracle

Welcome to the ESG Grid Oracle microservice! To ensure system stability and clean architecture, please follow these guidelines when contributing.

## Local Development Setup
1. Clone the repository and navigate into the directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: `make install`
4. Set up your `.env` file with a local `ESG_API_KEY`.

## Running the Service
Use the provided Makefile to spin up the local server:
```bash
make run