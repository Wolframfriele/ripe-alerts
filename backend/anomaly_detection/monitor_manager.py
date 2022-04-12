import os
import importlib
from django.forms.models import model_to_dict
from database.models import MeasurementCollection
from .monitor_strategy_base import MonitorStrategy
from .monitors import Monitor


class MonitorManager:
    def __init__(self):
        self.measurement_collection = MeasurementCollection.objects.all()
        self.monitors = dict()

        self.monitors = {}
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

        # for monitor in self.monitors.values():
        #     monitor.start()

    def create_monitors(self, measurements: list):
        # db.connections.close_all()
        for plugin in self._plugins:
            measurement_list = []
            measurement_list.append(measurements)
            for measurement in measurement_list:
                self.monitors = {}
                print(self.monitors)
                print(self.monitors.get(measurement.id))
                configuration_in_system = self.monitors.get(measurement.id) is None
                plugin_type_is_measurement_type = measurement.type == plugin.measurement_type()
                print('test test')
                print(configuration_in_system)
                print(plugin_type_is_measurement_type)
                if configuration_in_system and plugin_type_is_measurement_type:
                    print(1)
                    self.monitors[measurement.id] = Monitor(measurement, plugin)
                    self.monitors[measurement.id].start()


        # for plugin in self._plugins:
        #     for alert_configuration in alert_configurations:
        #         configuration_in_system = self.monitors.get(alert_configuration.alert_configuration_id) is None
        #         plugin_type_is_measurement_type = alert_configuration.measurement.type == plugin.measurement_type()
        #         if configuration_in_system and plugin_type_is_measurement_type:
        #             self.monitors[alert_configuration.alert_configuration_id] = Monitor(alert_configuration, plugin)
        #             self.monitors[alert_configuration.alert_configuration_id].start()

    def restart_monitor(self, monitor_id):
        pass

    def train_monitor_model(self, monitor_id):
        pass
