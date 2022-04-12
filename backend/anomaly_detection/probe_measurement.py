class ProbeMeasurement:
    def __init__(self, probe_id, created, entry_rtt, entry_ip, entry_as):
        self.probe_id = probe_id
        self.created = created
        self.entry_rtt = entry_rtt
        self.entry_ip = entry_ip
        self.entry_as = entry_as

    def __str__(self):
        return str(self.probe_id) + str(self.created)