from .models import AlertConfiguration
from .monitors import Monitor
from .monitor_strategies import PreEntryASMonitor
from .models import AlertConfiguration
from django import db


class MonitorManager:

    def __init__(self):

        self.alert_configurations = AlertConfiguration.objects.all()
        db.connections.close_all()
        self.monitors = dict()
        for alert_configuration in self.alert_configurations:
            # for i in range(10):
            #     print(alert_configuration.measurement.type)
            
            if alert_configuration.measurement.type == 'traceroute':
                strategy = PreEntryASMonitor()
                self.monitors[alert_configuration.measurement.measurement_id] = Monitor(alert_configuration, strategy)

        for monitor in self.monitors.values():
            monitor.start()

    def create_monitor(self, alert_configuration: AlertConfiguration):
        db.connections.close_all()
        if self.monitors.get(alert_configuration.alert_configuration_id) is None:
            if alert_configuration.measurement.type == 'Traceroute':
                strategy = PreEntryASMonitor()
                self.monitors[alert_configuration.measurement.measurement_id] = Monitor(alert_configuration, strategy)

    def restart_monitor(self, monitor_id):
        pass

    def train_monitor_model(self, monitor_id):
        pass
