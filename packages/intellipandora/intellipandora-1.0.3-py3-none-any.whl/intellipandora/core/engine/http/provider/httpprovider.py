# -*- coding: utf-8 -*-
"""
@Author: Shao Feng
@File  : httpprovider.py
@Time  : 2024-04-19
"""
from intellipandora.core.base.data.markdata import MarkData
from intellipandora.core.engine.http.provider.baseprovider import BaseProvider
from intellipandora.core.wrapper.requestwrapper import RequestWrapper
from intellipandora.core.wrapper.basewrapper import EndPointApiProxy


class HttpDesc(BaseProvider):

    def handle(self, path: str = '', mark: MarkData = '', method: str = '',
               params: dict = None, ori_params: dict = None):
        return RequestWrapper(path=path, mark=mark, method=method,
                              params=params or ori_params).build()


class Http(object):
    get = ''  # type:HttpDesc
    post = ''  # type:HttpDesc
    put = ''  # type:HttpDesc
    delete = ''  # type:HttpDesc
    options = ''  # type:HttpDesc
    patch = ''  # type:HttpDesc
    head = ''  # type:HttpDesc

    def __getattribute__(self, item):

        return HttpDesc(method=item)
