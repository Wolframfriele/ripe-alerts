from django.urls import path
from .apis import MyAtlasSystems, AtlasSearchSystems, SearchAsnNeighbours, UserAsnNeighbours

urlpatterns = [
    path('my-systems', MyAtlasSystems.as_view(), name="atlas-systems"),
    path('search-systems', AtlasSearchSystems.as_view(), name="atlas-search-systems"),
    path('search-neighbours', SearchAsnNeighbours.as_view()),
    path('my-neighbours', UserAsnNeighbours.as_view())
]
