.PHONY: isort black format build down run pycache_del start stop logs

# Запустить isort для сортировки импортов по всему проекту
isort:
	poetry run isort .

# Запустить black для форматирования кода по всему проекту
black:
	poetry run black .

# Запустить оба — isort, а потом black
format: isort black

# Запустить docker-compose
build:	
	docker compose up --build -d

down:
	docker-compose down

run:
	docker compose up -d
#uvicorn app.main:main_app --reload
start:
	docker compose start

stop:
	docker compose stop

logs:
	docker compose logs -f

pycache_del:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

test:
	docker compose -f docker-compose-test.yml up --build -d --remove-orphans
	docker compose -f docker-compose-test.yml exec -it test_app bash -c "pytest tests/ --maxfail=5 -v"


test-down:
	docker compose -f docker-compose-test.yml down