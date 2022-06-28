from telnetlib import STATUS
from django.shortcuts import render
from django.core import management
from django.core.management.commands import migrate
from ninja import Router, Query
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.core import serializers

from database.models import Notification

from .pluginplay.station import Station
from .database_interface import PostgresInterface
from notifications.api_schema import ConfigOut, ConfigFormat, ConfigFormatGet, AlertFormat

def setup():
    if not Station(PostgresInterface()):
        management.call_command('migrate')
    global station
    station = Station(PostgresInterface())

router = Router()
"""Tags are used by Swagger to group endpoints."""
NOTIFICATION_TAG = "Notification"

@router.post("/config", response=ConfigOut, tags=[NOTIFICATION_TAG])
def save_config(request, data: ConfigFormat = Query(...)):
    """Update the configuration of a plugin"""
    name = data.name
    config = data.config
    if name and config:
        station.save_plugin_config(name, config)
        return JsonResponse({"message":f"The plugin has been succesfully saved!"}, status=204)
    return JsonResponse({"message":"Invalid parameters!"}, status=400)

@router.get("/config", tags=[NOTIFICATION_TAG])
def get_config(request, data: ConfigFormatGet = Query(...)):
    """Get the configuration of a plugin"""
    name = data.plugin
    print(name)
    if not name:
        return JsonResponse({"message":"Missing parameter!"}, status=400)
    if name == "all":
        data = serializers.serialize('json', Notification.objects.all())
        print(len(data))
        return HttpResponse(data, content_type="application/json", status=200)

    data = serializers.serialize('json', Notification.objects.filter(name=name))
    return HttpResponse(data, content_type="application/json", status=200)

@router.post("/", tags=[NOTIFICATION_TAG])
def send_alert(request, data: AlertFormat = Query(...)):
    alert = data.alert
    if not alert:
        return JsonResponse({"message":"Missing parameter!"}, status=400)
    station.broadcast(alert)
    return JsonResponse({"message":"Succesfully send the alert!"}, status=204)


# class PluginConfigSystem(APIView):
#     def post(self, request: Request):
#         """Update the configuration of a plugin"""
#         name = request.POST.get("name")
#         config = request.POST.get("config")
#         if name and config:
#             station.save_plugin_config(name, config)
#             return Response(None, 204)
#         return Response("Invalid parameters", 400)

#     def get(self, request: Request):
#         """Get the configuration of a plugin"""
#         name = request.query_params.get("plugin")
#         if not name:
#             return Response("Missing parameter", 400)
#         if name == "all":
#             return Response(station.get_all_plugins_config(), 200, content_type="application/json")
#         return Response(station.get_plugin_config(name), 200, content_type="application/json")


# class AlertSystem(APIView):
#     def post(self, request: Request):
#         alert = request.POST.get("alert")
#         if not alert:
#             return Response("Missing parameter", 400)
#         station.broadcast(alert)
#         return Response(None, 204)
