from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from steam_trader import TraderClientObject
from steam_trader import exceptions

if TYPE_CHECKING:
    from ._client_ext import ExtClient
    from ._client_async_ext import ExtClientAsync

from collections import namedtuple
PriceRange = namedtuple('PriceRange', ['lowest', 'highest'])


@dataclass
class TradeMode(TraderClientObject):
    """Класс, представляющий режим торговли.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        state (:obj:`bool`): Режим обычной торговли.
        p2p (:obj:`bool`): Режим p2p торговли.
        client (Union[:class:`steam_trader.ExtClient`, :class:`steam_trader.ExtClientAsync`, :obj:`None`]):
                Клиент Steam Trader.
    """

    success: bool
    state: bool
    p2p: bool
    client: Union['ExtClient', 'ExtClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['ExtClient', 'ExtClientAsync', None] = None) -> 'TradeMode':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.ExtClient`, :class:`steam_trader.ExtClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.TradeMode`: Режим торговли.
        """

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 429:
                    raise exceptions.TooManyRequests('Вы отправили слишком много запросов.')

        data = super(TradeMode, cls).de_json(data)

        return cls(client=client, **data)

