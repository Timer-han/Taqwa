up:
	docker compose -f docker-compose.local.yml up -d --build

up_show:
	docker compose -f docker-compose.local.yml up --build

stop:
	docker compose -f docker-compose.local.yml stop

down:
	docker compose -f docker-compose.local.yml down

mongo-up:
	docker compose -f docker-compose.local.yml up -d mongodb

back-run:
	cd src && myenv/bin/python3 main.py