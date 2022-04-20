import datetime
import typing
from database.models import Probe
class ProbeMeasurement:
    def __init__(self, probe_id: int, created: datetime.datetime, entry_rtt, entry_ip: str, entry_as):
        self.probe_id = probe_id
        self.created = created
        self.entry_rtt = None
        self.entry_ip = entry_ip
        self.entry_as = None

    def save_to_database(self) -> None:
        probe = Probe.objects.create(probe=self.probe_id,
                                    measurement_id=7,
                                    as_number=1103, #dummy data
                                    location='Amsterdam') # dummy data
        probe.save()
        print(self)

    def __str__(self):
        return str(self.probe_id) + ' ' + str(self.created)


class Hops:
    def __init__(self, hop, ip, min_rtt):
        self.hop = hop
        self.ip_address = ip
        self.min_rtt = min_rtt

    def __str__(self):
        return str(self.hop) + str(self.ip) + str(self.min_rtt)