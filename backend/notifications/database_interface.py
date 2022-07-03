import typing
from urllib import request
from ripe_interface.api import get_username
from .pluginplay.interfaces.database import DatabaseInterface
from database.models import Notification, User, Setting


class PostgresInterface(DatabaseInterface):

    def __init__(self, *args, **kwargs):
        pass

    def save_plugin_config(self, name: str, config: typing.Dict[str, typing.Any]) -> None:
        user = User.objects.get(username=get_username(request))
        setting = Setting.objects.get(user=user)
        model = Notification()
        model.setting = setting
        model.name = name
        model.config = config
        model.save()

    def get_plugin_config(self, name: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
        notification = Notification.objects.filter(name=name)
        if len(notification) >= 1:
            return notification[0]
        else:
            return notification

    def get_all_plugin_configs(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        return Notification.objects.all()
