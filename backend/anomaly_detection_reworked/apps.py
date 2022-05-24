import threading

from django.apps import AppConfig

from anomaly_detection_reworked.measurement_result_stream import MeasurementResultStream


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