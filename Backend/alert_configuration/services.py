from .models import Anomaly


def get_anomalies(user_id, item):
    return Anomaly.objects.raw(
        """SELECT anomaly_id, is_alert, description, label, datetime
            FROM alert_configuration_anomaly as a
            JOIN alert_configuration_alertconfiguration as b ON b.alert_configuration_id = a.alert_configuration_id
            WHERE b.user_id = %s
            ORDER BY datetime DESC 
            LIMIT 20 OFFSET %s
        """, [user_id, item])


def get_alerts(user_id, item):
    return Anomaly.objects.raw(
        """SELECT anomaly_id, is_alert, description, label, datetime 
            FROM alert_configuration_anomaly as a
            JOIN alert_configuration_alertconfiguration as b ON b.alert_configuration_id = a.alert_configuration_id
            WHERE b.user_id = %s AND a.is_alert = true
            ORDER BY datetime DESC 
            LIMIT 20 OFFSET %s
        """, [user_id, item])
