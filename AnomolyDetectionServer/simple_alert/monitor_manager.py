from .monitors import Monitor, Measurement
from .monitor_strategies import PingMonitorStrategy, TracerouteMonitorStrategy
from typing import List

measurements = [Measurement(1042404, 'ping'), Measurement(1402318, 'ping'), Measurement(1423189, 'ping'),
                Measurement(1790205, 'traceroute'), Measurement(1789561, 'traceroute')]


class MonitorManager:

    def __init__(self):
        self.monitors = {
            1: Monitor(Measurement(1042404, 'ping'), None, PingMonitorStrategy()),
            2: Monitor(Measurement(1402318, 'ping'), None, PingMonitorStrategy()),
            3: Monitor(Measurement(1423189, 'ping'), None, PingMonitorStrategy()),
            4: Monitor(Measurement(1789561, 'traceroute'), None, TracerouteMonitorStrategy()),
            5: Monitor(Measurement(1790205, 'traceroute'), None, TracerouteMonitorStrategy()),
        }

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





