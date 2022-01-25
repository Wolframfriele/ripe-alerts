from .models import Anomaly
from django.db.models import QuerySet

# max items we return
MAX_ITEMS=20


def get_anomalies(user_id: int, item: int = 0) -> QuerySet:
    """Returns a QuerySet that contains all detected anomalies for the user

    Keyword arguments:
    user_id
    item -- offset (default 0)
    """
    return Anomaly.objects.raw(
        """SELECT anomaly_id, is_alert, description, label, datetime
            FROM alert_configuration_anomaly as a
            JOIN alert_configuration_alertconfiguration as b ON b.alert_configuration_id = a.alert_configuration_id
            WHERE b.user_id = %s
            ORDER BY datetime DESC 
            LIMIT 20 OFFSET %s
        """, [user_id, item])


def get_alerts(user_id: int, item: int = 0) -> QuerySet:
    """Returns a QuerySet that contains all detected alerts for the user

    Keyword arguments:
    user_id
    item -- offset (default 0)
    """
    return Anomaly.objects.raw(
        """SELECT anomaly_id, is_alert, description, label, datetime 
            FROM alert_configuration_anomaly as a
            JOIN alert_configuration_alertconfiguration as b ON b.alert_configuration_id = a.alert_configuration_id
            WHERE b.user_id = %s AND a.is_alert = true
            ORDER BY datetime DESC 
            LIMIT 20 OFFSET %s
        """, [user_id, item])
