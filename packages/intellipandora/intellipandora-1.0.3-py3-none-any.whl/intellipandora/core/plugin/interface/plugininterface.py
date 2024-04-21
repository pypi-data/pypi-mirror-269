# -*- coding: utf-8 -*-
"""
@Author: Shao Feng
@File  : plugininterface.py
@Time  : 2024-04-19
"""
from abc import ABCMeta

from intellipandora.core.base.data.markdata import MarkData
from intellipandora.core.engine.http.model.data.requestobject import RequestObject, SocketRequestObject
from intellipandora.core.engine.http.model.data.responseobject import ResponseObject, SocketResponseObject


class PluginInterface(metaclass=ABCMeta):

    def endpoints(self, mark: MarkData) -> dict: pass

    def request(self, request: RequestObject): pass

    def response(self, response: ResponseObject): pass

    def socketRequest(self, request: SocketRequestObject): pass

    def socketResponse(self, response: SocketResponseObject): pass
