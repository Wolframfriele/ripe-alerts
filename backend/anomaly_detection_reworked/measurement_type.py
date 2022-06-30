import enum


class MeasurementType(enum.Enum):
    PING = 1
    TRACEROUTE = 2
    DNS = 3
    HTTP = 4
    SSL = 5
    NTP = 6
    ANCHORING = 7
    WIFI = 8
    BUILT_IN = 9

    @classmethod
    def convert(cls, enum_str: str):
        enum_attr = getattr(cls, enum_str.upper())
        if not enum_attr:
            raise ValueError(
                "Enum incorrect, choose between: 'PING', TRACEROUTE', 'DNS', 'HTTP', 'SSL', "
                "'NTP', 'ANCHORING'.")
        return enum_str
