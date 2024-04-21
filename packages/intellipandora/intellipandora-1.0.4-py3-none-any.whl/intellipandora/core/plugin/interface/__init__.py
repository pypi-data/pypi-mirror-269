# -*- coding: utf-8 -*-
"""
@Author: Shao Feng
@File  : __init__.py.py
@Time  : 2024-04-19
"""
from intellipandora.core.plugin.interface.endpointsinterface import EndPointsInterface
from intellipandora.core.plugin.interface.httpregisterinterface import HttpPluginInterface
from intellipandora.core.plugin.interface.plugininterface import PluginInterface

__all__ = ['HttpPluginInterface', 'EndPointsInterface', 'PluginInterface']