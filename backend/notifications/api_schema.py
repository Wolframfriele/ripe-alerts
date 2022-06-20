from pydantic import Field
from ninja import Schema

class ConfigOut(Schema):
    message: str = Field(default="The plugin {name} has been succesfully saved!", description="Response from the server.")

class ConfigFormat(Schema):
    name: str = Field(default="Webhook", description="The name of the notification plugin")
    config: "JSONObject" = Field(default=None, description="The config of the plugin that was created")

class ConfigFormatGet(Schema):
    plugin: str = Field(default="Webhook", description="The name of the notification plugin")

class AlertFormat(Schema):
    alert: str = Field(default=None, description="The information of the alert that needs to be send")