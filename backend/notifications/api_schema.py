import json
from pydantic import Field
from ninja import Schema

config_example = {"description":"This a plugin to send message by using webhooks", 
                    "url":"http://localhost:8000/"}

config_output = {
    "model": "database.notification",
    "pk": 1,
    "fields": {
      "setting": 1,
      "name": "Webhook",
      "config": "{\"description\": \"This a plugin to send message by using webhooks\", \"url\": \"http://localhost:8000/\"}"
    }
  }

class ConfigOut(Schema):
    message: str = Field(default="The plugin has been succesfully saved!", description="Response from the server.")

class ConfigFormat(Schema):
    name: str = Field(default="Webhook", description="The name of the notification plugin")
    config: str = Field(default=json.dumps(config_example), description="The config of the plugin that was created")
    
class ConfigFormatGet(Schema):
    plugin: str = Field(default=None, description="The name of the notification plugin")

class AlertFormat(Schema):
    alert: str = Field(default=None, description="The information of the alert that needs to be send")