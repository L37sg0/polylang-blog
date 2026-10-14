ssl:
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
          -keyout ./nginx/ssl/wildcard.key \
          -out ./nginx/ssl/wildcard.crt \
          -subj "/CN=*.homecloud/O=Homecloud Local/C=BG"

up-initials:
	docker compose up -d nginx mysql adminer rabbitmq redis redis-commander meilisearch mailer

up-php:
	docker compose up -d php

up-js:
	docker compose up -d js

up-python:
	docker compose up -d python

down:
	docker compose down