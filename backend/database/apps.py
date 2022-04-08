from django.apps import AppConfig
from django.db import connection


class DatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'database'

    def ready(self):
        """To prevent: django.core.exceptions.AppRegistryNotReady-exception! Import after start-up!"""
        from django.contrib.auth.models import User
        auth_user_table_exist = "auth_user" in connection.introspection.table_names()
        if not auth_user_table_exist:
            return
        else:
            admin_exist = User.objects.filter(username="admin").exists()
            if not admin_exist:
                User.objects.create_superuser(username="admin", email="admin@ripe.net", password="password")
                print("Superuser 'admin' created!")