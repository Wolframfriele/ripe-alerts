from .models import Asn, Measurement
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


