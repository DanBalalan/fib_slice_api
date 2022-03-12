# fib_slice_api

Поднять контейнеры:
* docker-compose up --build

Роуты:
* http://127.0.0.1:5000/fibonacc

Зайти внутрь контейнеров:
* docker exec -ti fib_api-redis /bin/bash
* docker exec -ti fib_api-app /bin/bash

Тесты:
* docker exec -ti fib_api-app python -m pytest -v