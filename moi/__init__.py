# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import os

from redis import Redis
from future import standard_library
with standard_library.hooks():
    from configparser import ConfigParser

from moi.context import Context  # noqa


def _support_directory():
    """Get the path of the support_files directory"""
    from os.path import join, dirname, abspath
    return join(dirname(abspath(__file__)), 'support_files')


def moi_js():
    """Return the absolute path to moi.js"""
    from os.path import join
    return join(_support_directory(), 'moi.js')


def moi_list_js():
    """Return the absolute path to moi_list.js"""
    from os.path import join
    return join(_support_directory(), 'moi_list.js')


REDIS_KEY_TIMEOUT = 84600 * 14  # two weeks


# parse the config bits
_config = ConfigParser()
with open(os.environ['MOI_CONFIG_FP']) as conf:
    _config.readfp(conf)


# establish a connection to the redis server
r_client = Redis(host=_config.get('redis', 'host'),
                 port=_config.getint('redis', 'port'),
                 password=_config.get('redis', 'password'),
                 db=_config.get('redis', 'db'))


# setup contexts
ctxs = {name: Context(name)
        for name in _config.get('ipython', 'context').split(',')}
ctx_default = _config.get('ipython', 'default')

__version__ = '0.1.0-dev'
__all__ = ['r_client', 'ctxs', 'ctx_default', 'REDIS_KEY_TIMEOUT', 'moi_js',
           'moi_list_js']
