ssl:
	openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
          -keyout ./nginx/ssl/wildcard.key \
          -out ./nginx/ssl/wildcard.crt \
          -subj "/CN=*.homecloud/O=Homecloud Local/C=BG"