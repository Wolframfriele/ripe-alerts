import os
import typing
import importlib

from pluginplay.helpers.exceptions import NoValidParentClass
from pluginplay.interfaces.plugin import PluginInterface


class PluginLoader:
    """
    A class responsible for managing pluginplay plugins

    Attributes
    ---------
    _plugin_dir : DatabaseInterface
        An var which contains the name of the folder where the plugins are stored

    Methods
    -------
    discover_plugins()
        Check the provided folder for plugins/python files
    load_plugin(plugin_file)
        Returns an instance of the plugin
    initialize_plugin(plugin_file, config)
        Initializes the plugin with the given plugin
    """

    def __init__(self, plugin_dir: str):
        self._plugin_dir = plugin_dir

    def discover_plugins(self) -> typing.List[str]:
        """
        A function that discovers all the available plugins

        Returns
        -------
        A list that contains the name of all .py files found
        """

        plugins = os.listdir(self._plugin_dir)
        plugin_list = []
        for plugin in plugins:
            if plugin.endswith(".py"):
                plugin_list.append(plugin[:-3])
        return plugin_list

    def load_plugin(self, plugin_file: str) -> typing.Type[PluginInterface]:
        """
        A function that loads the given plugin

        Parameters
        ----------
        plugin_file : str
            The name of the python file which should contain the plugin

        Returns
        -------
        A instance of the given plugin, or an exception in the case of an invalid configuration
        """

        plugin = importlib.import_module(f"{self._plugin_dir}.{plugin_file}", ".")
        for key, value in plugin.__dict__.items():
            try:
                if issubclass(value, PluginInterface):
                    return value
            except TypeError:
                continue
        raise NoValidParentClass()

    def initialize_plugin(self, plugin_file: str, config: typing.Dict[str, typing.Any]) -> PluginInterface:
        """
        A function that initializes the given plugin

        Parameters
        ----------
        plugin_file : str
            The name of the python file which should contain the plugin
        config : dict[str, any]
            The config for the plugin

        Returns
        -------
        A instance of the given plugin, or an exception in the case of an invalid configuration
        """

        return self.load_plugin(plugin_file)(config)
