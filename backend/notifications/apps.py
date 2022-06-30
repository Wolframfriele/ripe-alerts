from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import os
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE_NOTIFICATIONSETUP')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE_NOTIFICATIONSETUP'] = 'True'  # Implement Locking

        import sys
        if 'migrate' in sys.argv:  # If we are migrating the database, do not start up anomaly detection.
            return
        from django.db import connection
        setting_table_exists = "database_setting" in connection.introspection.table_names()
        if not setting_table_exists:
            print("Start-up canceled. Migration is needed before the Anomaly Detection can be started.")
            return
        from .api import setup
        setup()
