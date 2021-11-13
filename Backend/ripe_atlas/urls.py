from django.urls import path
from .apis import MyAtlasSystems, AtlasSearchSystems

urlpatterns = [
    path('my-systems', MyAtlasSystems.as_view(), name="atlas-systems"),
    path('search-systems', AtlasSearchSystems.as_view(), name="atlas-search-systems"),
]
