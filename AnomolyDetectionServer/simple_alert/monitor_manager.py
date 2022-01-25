from .models import AlertConfiguration, Measurement
from .monitors import Monitor
from .monitor_strategies import PingMonitorStrategy, TracerouteMonitorStrategy, PreEntryASMonitor
from typing import List
from .models import AlertConfiguration
from django import db


class MonitorManager:

    def __init__(self):

        self.alert_configurations = AlertConfiguration.objects.all()
        db.connections.close_all()
        self.monitors = dict()
        for alert_configuration in self.alert_configurations:
            if alert_configuration.measurement.type == 'Ping':
                strategy = PingMonitorStrategy()
            else:
                strategy = PreEntryASMonitor()
            self.monitors[measurement.measurement_id] = Monitor(measurement, self.temporary_alert_config, strategy)

        for monitor in self.monitors.values():
            monitor.start()

    def create_monitor(self, alert_configuration: AlertConfiguration):
        db.connections.close_all()
        if self.monitors.get(alert_configuration.alert_configuration_id) is None:
            if alert_configuration.measurement.type == 'Ping':
                strategy = PingMonitorStrategy()
            else:
                strategy = PreEntryASMonitor()
            self.monitors[measurement.measurement_id] = Monitor(measurement, self.temporary_alert_config, strategy)

    def restart_monitor(self, monitor_id):
        pass

    def train_monitor_model(self, monitor_id):
        pass
