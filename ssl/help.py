"python manage.py runserver_plus --cert-file cert.pem --key-file key.pem 0.0.0.0:443"
"openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes"
