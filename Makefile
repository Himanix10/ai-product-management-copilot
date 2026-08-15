.PHONY: setup db run test docker-build docker-run clean

setup:
	pip install -r requirements.txt

db:
	python create_db.py

run:
	python main.py

test:
	pytest

docker-build:
	docker build -t ai-pm-copilot .

docker-run:
	docker-compose up --build -d

clean:
	rm -rf __pycache__ .pytest_cache logs/*.log