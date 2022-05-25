import threading

import django
from django.apps import AppConfig
from django.dispatch import receiver

# from django.core.signals import my_signal_handler
from anomaly_detection_reworked import server_shutdown_event
from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream


@receiver(server_shutdown_event)
def stop_anomaly_detection(sender, **kwargs):
    pass
    # print("Request finished!")


def start_anomaly_detection():
    # threading.Thread(target=MeasurementResultStream).start()
    print("Started Anomaly Detection!")


class AnomalyDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anomaly_detection_reworked'

    def ready(self):
        """ We first have to run multiple checks before starting up the anomaly detection module.
            First part of code is used to prevent Django for starting Anomaly Detection twice!
            Second part of code disables the anomaly detection module if we're running tests or migrating.
            Third part of code checks for a given start-up argument in order for the threads to work correctly."""
        import os
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'

        import sys
        if sys.argv is None:
            return
        if 'test' or 'migrate' in sys.argv:  # If we are unit testing or migrating the database, do not start up anomaly detection.
            return
        for argument in sys.argv:
            if argument == '--noreload':
                start_anomaly_detection() # --noreload option has to given in order for threads to work correctly.
                return
        print("Anomaly Detection disabled.")
        print("To enable this, please use the --noreload option at "
              "startup.")

    @receiver(server_shutdown_event)
    def lala(sender, **kwargs):
        pass
        # print("lalalala")
