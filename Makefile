.PHONY: install run test docker-up docker-down

install:
	pip install -r requirements.txt
	pip install pytest httpx

run:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest test_api.py -v

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down