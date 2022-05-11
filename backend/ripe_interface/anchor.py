from database.models import MeasurementCollection, AutonomousSystem, Tag


class Anchor:
    def __init__(self, id, type, fqdn, probe, is_ipv4_only, ip_v4, as_v4, ip_v4_gateway, ip_v4_netmask, ip_v6, as_v6,
                 ip_v6_gateway, ip_v6_prefix, city, country, company, nic_handle, geometry, tlsa_record, is_disabled,
                 date_live, hardware_version):
        self.id = id
        self.type = type
        self.fqdn = fqdn
        self.probe = probe
        self.is_ipv4_only = is_ipv4_only
        self.ip_v4 = ip_v4
        self.as_v4 = as_v4
        self.ip_v4_gateway = ip_v4_gateway
        self.ip_v4_netmask = ip_v4_netmask
        self.ip_v6 = ip_v6
        self.as_v6 = as_v6
        self.ip_v6_gateway = ip_v6_gateway
        self.ip_v6_prefix = ip_v6_prefix
        self.city = city
        self.country = country
        self.company = company
        self.nic_handle = nic_handle
        self.geometry = geometry
        self.tlsa_record = tlsa_record
        self.is_disabled = is_disabled
        self.date_live = date_live
        self.hardware_version = hardware_version

    def __str__(self) -> str:
        return "Anchor (id: " + str(self.id) + " | asn: " + str(self.as_v4) \
               + " | ip: " + self.ip_v4 + " | city: " + self.city + ")"


class AnchoringMeasurement:
    def __init__(self, id, type, interval, description, tags, target):
        self.id = id
        self.type = type
        self.interval = interval
        self.description = description
        self.tags = tags
        self.target = target

    def __str__(self):
        return self.description

    def save_to_database(self, system: AutonomousSystem):
        tags = Tag.get_tag_ids(self.tags)
        measurement_collection, created = MeasurementCollection.objects.get_or_create(
            autonomous_system=system, type=self.type, target=self.target, measurement_id=self.id,
            description=self.description)
        measurement_collection.tags.set(tags)
        return measurement_collection

