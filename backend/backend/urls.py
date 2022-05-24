"""RIPE Alerts URL Configuration
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from ninja import NinjaAPI
from ninja.security import django_auth

from anomaly_detection.api import router as anomaly_detection_router
from backend.settings import NINJA_AUTH_ENABLED as NINJA_AUTH_ENABLED
from ripe_interface.api import router as ripe_interface_router
from feedback.api import router as feedback_router


def api_redirect(request):
    return redirect('/api/docs#/')


def auth_configuration():
    if NINJA_AUTH_ENABLED:
        return django_auth
    elif not NINJA_AUTH_ENABLED:
        return None


description = ""
if NINJA_AUTH_ENABLED:
    description = "Welcome to our backend server!<br><br>Authentication is enabled. To change this, " \
                  "open <u>backend/settings.py</u> and set NINJA_AUTH_ENABLED to false.  <br></br>Go to: " \
                  "<a href='/admin/'>Django administration panel</a>"
elif not NINJA_AUTH_ENABLED:
    description = "Welcome to our backend server!<br><br>Authentication is disabled. To change this, " \
                  "open <u>backend/settings.py</u> and set NINJA_AUTH_ENABLED to true.  <br></br>Go to: " \
                  "<a href='/admin/'>Django administration panel</a>"

api = NinjaAPI(title="RIPE Alerts API", version="0.1", description=description, csrf=NINJA_AUTH_ENABLED)
api.add_router("/asn/", ripe_interface_router, auth=auth_configuration())
api.add_router("/ai/", anomaly_detection_router, auth=auth_configuration())
api.add_router("/feedback", feedback_router, auth=auth_configuration())
# api.add_router("/ai/", anomaly_detection_router, auth=auth_configuration())

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls, name='swagger'),
    path('', api_redirect, name='redirect-to-swagger')
    # path('monitor/', include('anomaly_detection.urls')) #TODO: fix migration bug
]
