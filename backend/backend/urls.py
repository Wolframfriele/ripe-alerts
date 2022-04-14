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
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import path
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView
from ninja import NinjaAPI
from ripe_interface.api import router as ripe_interface_router


description = "Welcome to our backend server!<br></br>Go to: " \
              "<a href='/admin/'>Django administration panel</a>"

api = NinjaAPI(title="Ripe Alerter API", version="0.1", description=description, csrf=True)
api.add_router("/asn/", ripe_interface_router)


def api_redirect(request):
    return redirect('/api/docs#/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls, name='swagger'),
    path('', api_redirect, name='redirect-to-swagger'),
    path('monitor/', include('anomaly_detection.urls')) #TODO: fix u need to remove this line bug: with this: setting_table_exists = "database_setting" in connection.introspection.table_names()
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api/atlas/', include('ripe_atlas.urls')),
    # path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/user/', include('users.urls')),
    # path('api/alert/', include('notifications.urls')),
    # path('api/alerts/', include('alert_configuration.urls'))
]
