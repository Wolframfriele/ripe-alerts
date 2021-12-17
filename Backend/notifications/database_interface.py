import typing
import json

from pluginplay.interfaces.database import DatabaseInterface
from .models import NotificationPlatform


class PostgresInterface(DatabaseInterface):

    def __init__(self, *args, **kwargs):
        pass

    def save_plugin_config(self, name: str, config: typing.Dict[str, typing.Any]) -> None:
        model = NotificationPlatform()
        model.notification_platform_name = name
        model.notification_platform_configuration = config
        model.save()

    def get_plugin_config(self, name: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
        return None
        return json.loads(NotificationPlatform.objects.filter(notification_platform_name=name).
                          values("notification_platform_configuration")[0].get("notification_platform_configuration"))

    def get_all_plugin_configs(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        return NotificationPlatform.objects.all().values("notification_platform_configuration")
