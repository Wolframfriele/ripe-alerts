import os

try:
    os.system("python manage.py createsuperuser --noinput --username admin --email admin@myproject.com")
except:
    print("Can't create that superuser!")