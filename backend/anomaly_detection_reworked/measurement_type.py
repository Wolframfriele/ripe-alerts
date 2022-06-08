import enum


class MeasurementType(enum.Enum):
    PING = 1
    TRACEROUTE = 2
    DNS = 3
    HTTP = 4
    SSL = 5
    NTP = 6
    ANCHORING = 7

    @staticmethod
    def convert(enum_str: str):
        enum_str = enum_str.upper()
        if enum_str == 'PING':
            return MeasurementType.PING
        elif enum_str == 'TRACEROUTE':
            return MeasurementType.TRACEROUTE
        elif enum_str == 'DNS':
            return MeasurementType.DNS
        elif enum_str == 'HTTP':
            return MeasurementType.HTTP
        elif enum_str == 'SSL':
            return MeasurementType.SSL
        elif enum_str == 'NTP':
            return MeasurementType.NTP
        elif enum_str == 'ANCHORING':
            return MeasurementType.ANCHORING
        else:
            raise ValueError("Enum incorrect, choose between: 'PING', TRACEROUTE', 'DNS', 'HTTP', 'SSL', "
                             "'NTP', 'ANCHORING'.")
