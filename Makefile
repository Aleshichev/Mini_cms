.PHONY: isort black format

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
	docker-compose up --build

down:
	docker-compose down