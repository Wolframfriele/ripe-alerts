from django.urls import path
from .views import MyAtlasProbes, AtlasSearchProbes, RelevantMeasurements

urlpatterns = [
    path('my-probes', MyAtlasProbes.as_view(), name="atlas-probes"),
    path('probes', AtlasSearchProbes.as_view(), name="atlas-search-probes"),
    path('measurements', RelevantMeasurements.as_view(), name='atlas-relevant-measurements'),
]
