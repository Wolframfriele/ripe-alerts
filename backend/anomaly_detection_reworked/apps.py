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
        """ To prevent Django for starting Anomaly Detection twice! """
        import os
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'

        import sys
        if sys.argv is None:
            return
        for argument in sys.argv:
            if argument == '--noreload':
                start_anomaly_detection()
                return
        print("Anomaly Detection disabled.")
        print("To enable this, please use the --noreload option at "
              "startup.")

    @receiver(server_shutdown_event)
    def lala(sender, **kwargs):
        pass
        # print("lalalala")