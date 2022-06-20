import typing

from .pluginplay.interfaces.database import DatabaseInterface
from database.models import Notification


class PostgresInterface(DatabaseInterface):

    def __init__(self, *args, **kwargs):
        pass

    def save_plugin_config(self, name: str, config: typing.Dict[str, typing.Any]) -> None:
        model = Notification()
        model.name = name
        model.config = config
        model.save()

    def get_plugin_config(self, name: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
        return Notification.objects.filter(name=name)

    def get_all_plugin_configs(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        return Notification.objects.all()
