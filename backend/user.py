import os
import importlib
import ripe-alerts-database

try:
    os.system("python manage.py createsuperuser --noinput --username admin --email admin@myproject.com")
except:
    pass

measurement = MeasurementCollection.objects.all()
print(measurement)