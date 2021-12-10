from django.urls import path
from .apis import MyAtlasSystems, AtlasSearchSystems, SearchAsnNeighbours, UserAsnNeighbours, Asn

urlpatterns = [
    path('my-systems', MyAtlasSystems.as_view(), name="atlas-systems"),
    path('search-systems', AtlasSearchSystems.as_view(), name="atlas-search-systems"),
    path('search-neighbours', SearchAsnNeighbours.as_view()),
    path('my-neighbours', UserAsnNeighbours.as_view()),
    path('asn', Asn.as_view())
]
