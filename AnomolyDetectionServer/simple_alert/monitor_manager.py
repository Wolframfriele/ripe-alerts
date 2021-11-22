from .monitors import Monitor, Measurement
from .monitor_strategies import PingMonitorStrategy, TracerouteMonitorStrategy
from typing import List

measurements = [Measurement(1042404, 'ping'), Measurement(1402318, 'ping'), Measurement(1423189, 'ping'),
                Measurement(1790205, 'traceroute')]


class MonitorManager:

    def __init__(self):
        self.monitors: List[Monitor] = []
        for measurement in measurements:
            if measurement.type == 'ping':
                self.monitors.append(Monitor(measurement, None, PingMonitorStrategy()))
            elif measurement.type == 'traceroute':
                self.monitors.append(Monitor(measurement, None, TracerouteMonitorStrategy()))

        for monitor in self.monitors:
            monitor.start()

    def create_monitor(self, measurement: Measurement):
        if measurement.type == "ping":
            self.monitors.append(Monitor(measurement=measurement, alert_configurations=None,
                                         strategy=PingMonitorStrategy()))
        elif measurement.type == "traceroute":
            self.monitors.append(Monitor(measurement=measurement, alert_configurations=None,
                                         strategy=TracerouteMonitorStrategy()))
        self.monitors[-1].start()





