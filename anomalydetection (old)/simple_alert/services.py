from .models import MeasurementCollection, AutonomousSystem
from django.db.models import QuerySet


def get_measurements(asn :str) -> QuerySet:
    return Measurement.objects.raw(
        """
        SELECT measurement_id, type
        FROM ripe_atlas_measurement AS a 
        JOIN ripe_atlas_anchor AS b ON b.anchor_id = a.anchor_id
        JOIN ripe_atlas_asn AS c on c.asn = b.asn_id
        WHERE b.asn_id = %s
        """, [asn]
    )


def get_measurementcollection_by_asn(asn: str) -> QuerySet:
    return MeasurementCollection.objects.raw(
        """
        SELECT *
        FROM database_MeasurementCollection 
        WHERE autonomous_system_id = %s
        """, [asn]
    )
   
    # return AlertConfiguration.objects.raw(
    #     """
    #     SELECT *
    #     FROM ripe_atlas_measurement AS a 
    #     JOIN ripe_atlas_anchor AS b ON b.anchor_id = a.anchor_id
    #     JOIN ripe_atlas_asn AS c on c.asn = b.asn_id
    #     JOIN alert_configuration_alertconfiguration aca on a.measurement_id = aca.measurement_id
    #     WHERE b.asn_id = %s
    #     """, [asn]
    # )