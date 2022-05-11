from django.shortcuts import render
from django.core import management
from django.core.management.commands import migrate
# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from pluginplay.station import Station
from .database_interface import PostgresInterface

if not Station(PostgresInterface()):
    management.call_command('migrate')
station = Station(PostgresInterface())

class PluginConfigSystem(APIView):
    def post(self, request: Request):
        """Update the configuration of a plugin"""
        name = request.POST.get("name")
        config = request.POST.get("config")
        if name and config:
            station.save_plugin_config(name, config)
            return Response(None, 204)
        return Response("Invalid parameters", 400)

    def get(self, request: Request):
        """Get the configuration of a plugin"""
        name = request.query_params.get("plugin")
        if not name:
            return Response("Missing parameter", 400)
        if name == "all":
            return Response(station.get_all_plugins_config(), 200, content_type="application/json")
        return Response(station.get_plugin_config(name), 200, content_type="application/json")


class AlertSystem(APIView):
    def post(self, request: Request):
        alert = request.POST.get("alert")
        if not alert:
            return Response("Missing parameter", 400)
        station.broadcast(alert)
        return Response(None, 204)
