# -*- coding: utf-8 -*-
"""
@Author: Shao Feng
@File  : pluginmanager.py
@Time  : 2024-04-19
"""
from intellipandora.core.plugin.innerplugin import InnerPlugin
from intellipandora.core.plugin.specificationsbuilder import SpecificationsManager
from intellipandora.core.plugin.interface.endpointsinterface import EndPointsInterface
from intellipandora.core.plugin.interface.httpregisterinterface import HttpPluginInterface
from intellipandora.core.plugin.interface.plugininterface import PluginInterface


class PluginManager(object):

    @classmethod
    def init(cls):
        cls.register(InnerPlugin())

    @classmethod
    def http(cls, reg: HttpPluginInterface = None):
        cls.register(reg)

    @classmethod
    def endpoints(cls, reg: EndPointsInterface = None):
        cls.register(reg)

    @classmethod
    def register(cls, plugin: PluginInterface = None):
        cls.get_builder().add_register(plugin)

    @classmethod
    def run(cls, method=None, *args, **kwargs):
        return cls.get_builder().run(method=method, *args, **kwargs)

    @classmethod
    def get_builder(cls):
        return SpecificationsManager.get_builder(tag='default_plugin', interface=PluginInterface)
