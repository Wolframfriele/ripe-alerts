import os
import importlib
from django.forms.models import model_to_dict
from database.models import MeasurementCollection
from .monitor_strategy_base import MonitorStrategy
from .monitors import Monitor


class MonitorManager:
    #Get all plugin and check if excisting measurementcollections needs to be monitored 
    def __init__(self):
        self.measurement_collection = MeasurementCollection.objects.all()
        self.monitors = dict()

        print("Monitor Manager started.")
        print(self.monitors)
        
        plugins = os.listdir('anomaly_detection/detection_methods')
        plugin_list = []
        for plugin in plugins:
            if plugin.endswith(".py") and plugin != '__init__.py':
                plugin_list.append(plugin[:-3])

        self._plugins = [
            importlib.import_module(f'anomaly_detection.detection_methods.{plugin}').DetectionMethod() for plugin in plugin_list
        ]

        for plugin in self._plugins:
            if isinstance(plugin, MonitorStrategy):
                for measurement in self.measurement_collection:
                    if measurement.type == plugin.measurement_type():
                        self.monitors[measurement.id] = Monitor(measurement, plugin)
            else:
                raise TypeError("Plugin does not follow MonitorStrategy")

        for monitor in self.monitors.values():
            monitor.start()

    #Check if plugin matches measurementcollection type and start the streaming API monitor
    def create_monitors(self, measurements: list):
        for plugin in self._plugins:
            measurement_list = []
            measurement_list.append(measurements)
            for measurement in measurement_list:
                configuration_in_system = self.monitors.get(measurement.id) is None
                plugin_type_is_measurement_type = measurement.type == plugin.measurement_type()
                if configuration_in_system and plugin_type_is_measurement_type:
                    self.monitors[measurement.id] = Monitor(measurement, plugin)
                    self.monitors[measurement.id].start()


    def restart_monitor(self, monitor_id):
        pass

    def train_monitor_model(self, monitor_id):
        pass
