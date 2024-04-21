# -*- coding: utf-8 -*-
"""
@Author: Shao Feng
@File  : __init__.py.py
@Time  : 2024-04-19
"""
from intellipandora.core.engine.http.provider import Http, Mark
from intellipandora.core.plugin import PluginManager
from intellipandora.core.base.classwrap.multihandle import init as exit_init
from intellipandora.core.engine.http.model.interface.responseinterface import HttpResponseInterface

# init plugin manager
PluginManager.init()

# init exit
exit_init()


class Api(object):
    http = Http()
    mark = Mark
    # socket = Socket()
    # data object
    response = None  # type:HttpResponseInterface
