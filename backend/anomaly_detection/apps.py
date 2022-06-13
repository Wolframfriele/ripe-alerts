import types
from typing import Optional
from django.apps import AppConfig
import sys
import os

from django.utils import tree
import threading

class AnomalyDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'anomaly_detection'
    
    def __init__(self, app_name: str, app_module: Optional[types.ModuleType]) -> None:
        super().__init__(app_name, app_module)
        self.started = False

    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        print(run_once)
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
        
        print(sys.argv)
        if sys.argv is None:
            return
        if 'migrate' in sys.argv:  # If we are migrating the database, do not start up the measurement monitoring.
            return
        if '--noreload' in sys.argv:
            from anomaly_detection.monitor_manager import MonitorManager
            thread = threading.Thread(target=MonitorManager, daemon=True)
            thread.start()
            print("Starting new thread!")
            return
        print("No measurements are being monitored!")
        print("To enable this, please use the --noreload option at "
              "startup.")