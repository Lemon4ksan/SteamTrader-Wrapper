import logging
from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from .exceptions import BadRequestError, Unauthorized, NoBuyOrders, TooManyRequests
from ._base import TraderClientObject
from ._misc import InventoryItem, BuyOrder, Discount, OperationsHistoryItem, AltWebSocketMessage

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync


@dataclass
class WebSocketToken(TraderClientObject):
    """Класс, представляющий WebSocket токен. Незадокументированно.

    Attributes:
        steam_id: (:obj:`str`)
        time: (:obj:`int`)
        hash: (:obj:`str`)
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    steam_id: str
    time: int
    hash: str
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['WebSocketToken']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.WebSocketToken`, optional: WebSocket токен.
        """

        if not cls.is_valid_model_data(data):
            return

        try:
            if not data['success']:
                match data['code']:
                    case 401:
                        raise Unauthorized('Вы не зарегистрированны.')
                    case 429:
                        raise TooManyRequests('Вы отправили слишком много запросов.')
        except KeyError:
            pass

        data = super(WebSocketToken, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class Inventory(TraderClientObject):
    """Класс, представляющий инвентарь клиента.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        count (:obj:`int`): Количество всех предметов в инвентаре Steam.
        gameid (:obj:`int`): AppID игры к которой принадлежит инвентарь.
        last_update (:obj:`int`): Timestamp последнего обновления инвентаря.
        items (Sequence[:class:`steam_trader.InventoryItem`, optional]): Последовательность с предметами в инвентаре.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    count: int
    gameid: int
    last_update: int
    items: Sequence[Optional['InventoryItem']]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            status: Optional[Sequence[int]] = None,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['Inventory']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            status (Sequence[:obj:`int`], optional): Указывается, чтобы получить список предметов с определенным статусом.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Inventory`, optional: Инвентарь клиента.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            try:
                match data['code']:
                    case 400:
                        raise BadRequestError('Неправильный запрос.')
                    case 401:
                        raise Unauthorized('Неправильный api-токен.')
                    case 429:
                        raise TooManyRequests('Вы отправили слишком много запросов.')
            except KeyError:
                pass

        data.update({
            'gameid': data['game']
        })
        del data['game']

        if status is not None:
            new_data = []
            for i, offer in enumerate(data['items']):
                if offer['status'] in status:
                    new_data.append(InventoryItem.de_json(offer))

            data['items'] = new_data
        else:
            for i, offer in enumerate(data['items']):
                data['items'][i] = InventoryItem.de_json(offer)

        data = super(Inventory, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class BuyOrders(TraderClientObject):
    """Класс, представляющий ваши запросы на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (Sequence[:class:`steam_trader.BuyOrder`, optional]): Последовательность запросов на покупку.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    data: Sequence[Optional['BuyOrder']]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['BuyOrders']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyOrders`, optional: Ваши запросы на покупку.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос.')
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')
                case 1:
                    raise NoBuyOrders('Нет запросов на покупку.')

        for i, offer in enumerate(data['data']):
            data['data'][i] = BuyOrder.de_json(offer)

        data = super(BuyOrders, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class Discounts(TraderClientObject):
    """Класс, представляющий комиссии/скидки на игры, доступные на сайте.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (dict[:obj:`int`, :class:`steam_trader.Discount`, optional]): Словарь, содержащий комисии/скидки.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    data: dict[int, Optional['Discount']]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['Discounts']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Discounts, optional`: Комиссии/скидки на игры.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос.')
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')

        # Конвертируем ключ в число для совместимости с константами
        data['data'] = {int(appid): Discount.de_json(_dict) for appid, _dict in data['data'].items()}
        data = super(Discounts, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class OperationsHistory(TraderClientObject):
    """Класс, представляющий истории операций, произведённых на сайте.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (Sequence[:class:`steam_trader.OperationsHistoryItem`, optional]): Последовательность историй операций.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    data: Sequence[Optional['OperationsHistoryItem']]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['OperationsHistory']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Discounts`, optional: Истории операций.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос.')
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')

        for i, item in enumerate(data['data']):
            data['data'][i] = OperationsHistoryItem.de_json(item)

        data = super(OperationsHistory, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class InventoryState(TraderClientObject):
    """Класс, представляющий текущий статус инвентаря.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        updating_now (:obj:`bool`): Инвентарь обновляется в данный момент.
        last_update (:obj:`int`): Timestamp, когда последний раз был обновлён инвентарь.
        items_in_cache (:obj:`int`): Количество предметов в инвентаре.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    updating_now: bool
    last_update: int
    items_in_cache: int
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['InventoryState']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.InventoryState`, optional: Текущий статус инвентаря.
        """

        if not cls.is_valid_model_data(data):
            return

        data.update({  # перенос с camleCase на snake_case
            'updating_now': data['updatingNow'],
            'last_update': data['lastUpdate'],
            'items_in_cache': data['itemsInCache']
        })
        del data['updatingNow'], data['lastUpdate'], data['itemsInCache']

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос.')
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')

        data = super(InventoryState, cls).de_json(data)

        return cls(client=client, **data)


@dataclass
class AltWebSocket(TraderClientObject):
    """Класс, представляющий запрос альтернативным WebSocket.

    Attributes:
        success (:obj:`bool`): Результат запроса. Если false, сообщений в поле messages не будет,
            при этом соединение будет поддержано.
        messages (Sequence[:class:`steam_trader.AltWebSocketMessage`, optional]):
            Последовательность с WebSocket сообщениями.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    messages: Sequence[Optional['AltWebSocketMessage']]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> Optional['AltWebSocket']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.AltWebSocket`, optional: Запрос альтернативным WebSocket.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            logging.warning('WebSocket соединение поддержано.')
            return

        for i, message in enumerate(data['messages']):
            data['messages'][i] = AltWebSocketMessage.de_json(message)

        data = super(AltWebSocket, cls).de_json(data)

        return cls(client=client, **data)
