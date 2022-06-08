import enum


class MeasurementType(enum.Enum):
    PING = 1
    TRACEROUTE = 2
    DNS = 3
    HTTP = 4
    SSL = 5
    NTP = 6
    ANCHORING = 7
