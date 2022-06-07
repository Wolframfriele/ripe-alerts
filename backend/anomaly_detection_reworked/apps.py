import threading

import django
from django.apps import AppConfig
from django.dispatch import receiver

# from django.core.signals import my_signal_handler
from anomaly_detection_reworked import server_shutdown_event
from anomaly_detection_reworked.anomaly_detection import AnomalyDetection
from anomaly_detection_reworked.detection_methods import entry_point_delay
# from anomaly_detection_reworked.anomaly_detection import anchor_down
from anomaly_detection_reworked.detection_methods.delay_from_country import DelayFromCountry
from anomaly_detection_reworked.detection_methods.entry_point_delay import EntryPointDelay
from anomaly_detection_reworked.detection_methods.anchor_down import AnchorDown
from anomaly_detection_reworked.detection_methods.neighbor_network_delay import NeighborNetworkDelay
from anomaly_detection_reworked.detection_methods.route_change import RouteChange
from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream

anomaly_detection = AnomalyDetection()

anomaly_detection.add_detection_method(EntryPointDelay)
anomaly_detection.add_detection_method(AnchorDown)
anomaly_detection.add_detection_method(RouteChange)
anomaly_detection.add_detection_method(NeighborNetworkDelay)
anomaly_detection.add_detection_method(DelayFromCountry)


@receiver(server_shutdown_event)
def stop_anomaly_detection(sender, **kwargs):
    print("Stopping Anomaly Detection!")
    anomaly_detection.stop()


def start_anomaly_detection():
    print("Started Anomaly Detection!")
    anomaly_detection.start()


class AnomalyDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anomaly_detection_reworked'

    def ready(self):
        """ When you use 'python manage.py runserver' Django starts two processes, one for the actual development server
            and other to reload your application when the code changes. Because of this, this method is called twice.
        Read: https://stackoverflow.com/questions/33814615/how-to-avoid-appconfig-ready-method-running-twice-in-django
            We have to run multiple checks before starting up the anomaly detection app.
            First part of code is used to prevent Django for starting Anomaly Detection twice!
            Second part of code disables the anomaly detection app if we're running tests or migrating.
            """
        import os
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'  # Implement Locking

        import sys
        if 'migrate' in sys.argv:  # If we are migrating the database, do not start up anomaly detection.
            return
        elif 'test' in sys.argv:  # If we are running tests, do not start up anomaly detection
            return
        start_anomaly_detection()
