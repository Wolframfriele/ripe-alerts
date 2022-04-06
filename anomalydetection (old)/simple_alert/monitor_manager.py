import os
import importlib
from .monitor_strategy_base import MonitorStrategy
from .models import AlertConfiguration
from .monitors import Monitor
from .models import AlertConfiguration
from django import db


class MonitorManager:
    def __init__(self):
        self.alert_configurations = AlertConfiguration.objects.all()
        db.connections.close_all()
        self.monitors = dict()
        
        plugins = os.listdir('simple_alert/DetectionMethods')
        plugin_list = []
        for plugin in plugins:
            if plugin.endswith(".py") and plugin != '__init__.py':
                plugin_list.append(plugin[:-3])

        self._plugins = [
            importlib.import_module(f'simple_alert.DetectionMethods.{plugin}').DetectionMethod() for plugin in plugin_list
        ]

        for plugin in self._plugins:
            if isinstance(plugin, MonitorStrategy):
                for alert_configuration in self.alert_configurations:
                    if alert_configuration.measurement.type == plugin.measurement_type():
                        print(alert_configuration)
                        self.monitors[alert_configuration.alert_configuration_id] = Monitor(alert_configuration, plugin)
            else:
                raise TypeError("Plugin does not follow MonitorStrategy")

        for monitor in self.monitors.values():
            monitor.start()

    def create_monitors(self, alert_configurations: list):
        db.connections.close_all()
        for plugin in self._plugins:
            for alert_configuration in alert_configurations:
                configuration_in_system = self.monitors.get(alert_configuration.alert_configuration_id) is None
                plugin_type_is_measurement_type = alert_configuration.measurement.type == plugin.measurement_type()
                if configuration_in_system and plugin_type_is_measurement_type:
                    self.monitors[alert_configuration.alert_configuration_id] = Monitor(alert_configuration, plugin)
                    self.monitors[alert_configuration.alert_configuration_id].start()

    def restart_monitor(self, monitor_id):
        pass

    def train_monitor_model(self, monitor_id):
        pass
