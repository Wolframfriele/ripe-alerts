import typing

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
        return NotificationPlatform.objects.filter(notification_platform_name=name)

    def get_all_plugin_configs(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        return NotificationPlatform.objects.all()
