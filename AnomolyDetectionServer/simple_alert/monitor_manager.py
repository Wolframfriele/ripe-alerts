from .models import AlertConfiguration, Measurement
from .monitors import Monitor
from .monitor_strategies import PingMonitorStrategy, TracerouteMonitorStrategy, PreEntryASMonitor

from typing import List


class MonitorManager:

    def __init__(self):

        measurements = Measurement.objects.all()
        self.temporary_alert_config = AlertConfiguration.objects.first()

        self.monitors = dict()
        for measurement in measurements:
            if measurement.type == 'Ping':
                strategy = PingMonitorStrategy()
            else:
                strategy = TracerouteMonitorStrategy()
            self.monitors[measurement.measurement_id] = Monitor(measurement, self.temporary_alert_config, strategy)

        for monitor in self.monitors.values():
            monitor.start()

    def create_monitor(self, measurement: Measurement, alert_configurations=None):
        if self.monitors.get(measurement.measurement_id) is None:
            if measurement.type == 'Ping':
                strategy = PingMonitorStrategy()
            else:
                strategy = TracerouteMonitorStrategy()
            self.monitors[measurement.measurement_id] = Monitor(measurement, self.temporary_alert_config, strategy)

            self.monitors[measurement.measurement_id].start()

    def restart_monitor(self, monitor_id):

        pass

    def train_monitor_model(self, monitor_id):
        pass





