=====
Ripe_alerts_database
=====

This is the database for the ripe alerts.

Quick start
-----------

1. Add "database" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'database',
    ]

2. Run ``python manage.py migrate`` to create the database models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).
