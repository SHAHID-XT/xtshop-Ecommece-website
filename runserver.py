from waitress import serve
from ecommerce.wsgi import application  # Import your WSGI application
import os
import threading

os.system(
    "python manage.py runserver_plus --cert-file ./ssl/cert.pem --key-file ./ssl/key.pem --nopin 0.0.0.0:443 "
)
