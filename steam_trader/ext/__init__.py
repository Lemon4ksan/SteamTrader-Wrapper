"""Расширенная версия клиента с изменёнными методами"""

from ._client_ext import ExtClient
from ._client_async_ext import ExtClientAsync

__all__ = [
    'ExtClient',
    'ExtClientAsync'
]
