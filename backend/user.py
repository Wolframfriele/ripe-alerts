import os
import importlib

try:
    os.system("python manage.py createsuperuser --noinput --username admin --email admin@myproject.com")
except:
    pass
