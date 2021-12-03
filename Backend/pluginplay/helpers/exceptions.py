"""
This module contains all the custom exceptions

All the custom exceptions that the pluginplay package can throw are stored here.
"""


class NoValidParentClass(Exception):
    """Raised when a plugin has no class inherited from PluginInterface"""
    pass
