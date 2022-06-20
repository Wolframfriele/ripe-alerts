from django.shortcuts import render
from django.core import management
from django.core.management.commands import migrate
from ninja import Router, Query
from django.http import JsonResponse


from .pluginplay.station import Station
from .database_interface import PostgresInterface
from notifications.api_schema import ConfigOut, ConfigFormat, ConfigFormatGet, AlertFormat

if not Station(PostgresInterface()):
    management.call_command('migrate')
station = Station(PostgresInterface())

router = Router()
"""Tags are used by Swagger to group endpoints."""
NOTIFICATION_TAG = "Notification"

@router.post("/config", response=ConfigOut, tags=[NOTIFICATION_TAG])
def save_config(request, data: ConfigFormat):
    """Update the configuration of a plugin"""
    name = data.name
    config = data.config
    if name and config:
        station.save_plugin_config(name, config)
        return JsonResponse(None, status=204)
    return JsonResponse("Invalid parameters", status=400)

@router.get("/config", tags=[NOTIFICATION_TAG])
def get_config(request, data: ConfigFormatGet):
    """Get the configuration of a plugin"""
    name = data.plugin
    if not name:
        return JsonResponse("Missing parameter", status=400)
    if name == "all":
        return JsonResponse(station.get_all_plugins_config(), status=200, content_type="application/json")
    return JsonResponse(station.get_plugin_config(name), status=200, content_type="application/json")

@router.post("/", tags=[NOTIFICATION_TAG])
def send_alert(request, data: AlertFormat):
    alert = data.alert
    if not alert:
        return JsonResponse("Missing parameter", status=400)
    station.broadcast(alert)
    return JsonResponse(None, status=204)


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
