from .monitors import Monitor
from .monitor_strategies import PingMonitorStrategy, TracerouteMonitorStrategy
from .models import Measurement, AlertConfiguration
from typing import List


class MonitorManager:

    def __init__(self):
        measurements = Measurement.objects.all()
        temporary_alert_config = AlertConfiguration.objects.first()
        print(temporary_alert_config)

        self.monitors = dict()
        for measurement in measurements:
            if measurement.type == 'Ping':
                strategy = PingMonitorStrategy()
            else:
                strategy = TracerouteMonitorStrategy()
            self.monitors[measurement.measurement_id] = Monitor(measurement, temporary_alert_config, strategy)

        for monitor in self.monitors.values():
            monitor.start()

    def create_monitor(self, measurement: Measurement, alert_configurations=None):
        if measurement.type == "ping":
            self.monitors.append(Monitor(measurement=measurement, alert_configurations=alert_configurations,
                                         strategy=PingMonitorStrategy()))
        elif measurement.type == "traceroute":
            self.monitors.append(Monitor(measurement=measurement, alert_configurations=alert_configurations,
                                         strategy=TracerouteMonitorStrategy()))
        self.monitors[-1].start()

    def restart_monitor(self, monitor_id):

        pass

    def train_monitor_model(self, monitor_id):
        pass





