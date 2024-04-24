from __future__ import absolute_import

from .config import configure as __configure


def get_configure():
    return __configure


__all__ = ['get_configure']
