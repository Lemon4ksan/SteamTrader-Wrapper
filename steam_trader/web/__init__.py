"""
SteamTrader-Wrapper
~~~~~~~~~~~~~~~~~~~~~

Web scraper for Steam-Trader. Requires beutifulsoup4 and lxml

Licensed under the BSD 3-Clause License - Copyright (c) 2024-present, Lemon4ksan (aka Bananchiki) <https://github.com/Lemon4ksan>
See LICENSE
"""

from ._base import WebClientObject

from ._client import WebClient
from ._client_async import WebClientAsync

from ._dataclasses import MainPage
from ._dataclasses import MainPageItem
from ._dataclasses import ItemDescription
from ._dataclasses import ItemInfo
from ._dataclasses import SellOffer
from ._dataclasses import Referal
from ._dataclasses import HistoryItem

__all__ = [
    'WebClientObject',
    'WebClient',
    'MainPage',
    'MainPageItem',
    'ItemDescription',
    'ItemInfo',
    'SellOffer',
    'Referal',
    'HistoryItem'
]
