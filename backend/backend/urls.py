"""RipeUgh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from ripe_interface.api import router as events_router

api = NinjaAPI(title="Ripe Alerter API", version="0.1", description="Welcome to our backend server!",)
api.add_router("/asn/", events_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/atlas/', include('ripe_atlas.urls')),
    # path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/user/', include('users.urls')),
    # path('api/alert/', include('notifications.urls')),
    # path('api/alerts/', include('alert_configuration.urls'))
]
