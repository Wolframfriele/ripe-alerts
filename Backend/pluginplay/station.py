"""
This is the main class for managing plugins

This class is responsible for discovering and loading plugins.
It provides methods for getting and setting the configurations of plugins,
as well as broadcasting data to the plugins.
This is also the reason that it is called station, for radio broadcasting station.
"""

import typing

from pluginplay.helpers.exceptions import NoValidParentClass
from pluginplay.interfaces.database import DatabaseInterface
from pluginplay.plugin_loader import PluginLoader


class Station:
    """
    A class responsible for managing pluginplay plugins

    Attributes
    ---------
    _database_interface : DatabaseInterface
        An interface for storing and loading configs for plugins
    _plugin_manager : PluginLoader
        An interface for actively dealing with plugins
    _plugin_list : list[str]
        A list that contains all the discovered potential plugins
    _plugins : dict[str, PluginInterface]
        A dict that contains all the active instances of the plugins

    Methods
    -------
    broadcast(data)
        Sends the data to all loaded plugins
    get_plugin_config(name)
        Returns the actively used config of the given plugin
    get_all_plugins_config()
        Return the config for all loaded plugins at once
    save_plugin_config(name, config)
        Saves the given config in the database, and reloads the plugin as well
    reload_plugin(name, config)
        Reload the plugin with the given config
    """

    def __init__(self, database_interface: DatabaseInterface, plugin_dir: str = "plugins"):
        """
        Initializes the class and load found plugins.

        The initializer will initialize required components, and then start looking for and
        actively loading plugins when they are found.

        Parameters
        ----------
        database_interface : DatabaseInterface, required
            An interface that interfaces to the database for loading and saving configs
        plugin_dir : str, optional
            The directory where the plugins are stored
        """

        self._database_interface = database_interface
        self._plugin_manager = PluginLoader(plugin_dir)

        self._plugin_list = self._plugin_manager.discover_plugins()
        self._plugins = {}

        for plugin in self._plugin_list:
            try:
                plugin_class = self._plugin_manager.load_plugin(plugin)
            except NoValidParentClass:
                print(f"{plugin} does not follow the requirements for a plugin, skipping.")
                continue
            plugin_config = self._database_interface.get_plugin_config(plugin_class.NAME)
            if plugin_config:
                self._plugins[plugin_class.NAME] = plugin_class(plugin_config)
            else:
                self._plugins[plugin_class.NAME] = plugin_class(plugin_class.DEFAULT_CONFIG)

    def broadcast(self, data: typing.Any) -> None:
        """
        The method responsible for distributing data to plugins

        Parameters
        ----------
        data : any, required
            The data to be send to the plugins
        """

        for plugin in self._plugins.values():
            plugin.receiver(data)

    def get_plugin_config(self, name: str) -> typing.Union[typing.Dict[str, typing.Any], None]:
        """
        This method is responsible for returning the active plugin config

        Parameters
        ----------
        name : str, required
            The name of the plugin for which the config needs to be collected

        Returns
        -------
        A dictionary containing the name, description and config of the given plugin
        """

        if config := self._database_interface.get_plugin_config(name):
            return {
                "name": name,
                "description": self._plugins.get(name).DESCRIPTION,
                "config": config
            }
        return {
            "name": name,
            "description": self._plugins.get(name).DESCRIPTION,
            "config": self._plugins.get(name).DEFAULT_CONFIG
        }

    def get_all_plugins_config(self) -> typing.List[typing.Union[typing.Dict[str, typing.Any], None]]:
        """
        This method is responsible for returning the active plugin config of all plugins

        Returns
        -------
        A list containing dictionary containing the name, description and config of the given plugin
        """

        return [self.get_plugin_config(plugin) for plugin in self._plugins]

    def save_plugin_config(self, name: str, config: typing.Dict[str, typing.Any]) -> None:
        """
        This method is responsible for saving the new config, and reloading the plugin

        Parameters
        ----------
        name : str
            The name of the plugin
        config : dict[str, any]
            The new config
        """

        self._database_interface.save_plugin_config(name, config)
        self.reload_plugin(name, config)

    def reload_plugin(self, name: str, config: typing.Union[typing.Dict[str, typing.Any], None]) -> None:
        """
        This method reloads the given plugin with the given plugin

        Parameters
        ----------
        name : str
            The name of the plugin
        config : dict[str, any]
            The new config
        """

        for plugin in self._plugin_list:
            try:
                plugin_class = self._plugin_manager.load_plugin(plugin)
            except NoValidParentClass:
                print(f"{plugin} does not follow the requirements for a plugin, skipping.")
                continue
            self._plugins[name] = plugin_class(config)
