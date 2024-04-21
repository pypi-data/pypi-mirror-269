# -*- coding: utf-8 -*-
# @Author: Shao Feng
# @File  : __init__.py.py
# @Time  : 2024-04-17
import logging
import os
import sys
from intellipandora.core.schedule.runtime import Runtime
from intellipandora.core.engine.http import Api

null_handler = logging.NullHandler()
logging.root.setLevel(logging.INFO)
logging.root.addHandler(null_handler)

# 获取logger对象
logger = logging.getLogger(__name__)
logger.propagate = False

# 全局formatter
formatter = logging.Formatter(
    '[%(asctime)s]%(process)s(%(levelname)s)%(name)s : %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 注册handler
logger.addHandler(console_handler)

logger = logging.getLogger(__name__)

api = Api()


def init(product=''):
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    Runtime.product = product


__all__ = ['api', 'init']
