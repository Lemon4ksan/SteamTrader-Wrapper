from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence, Dict

from steam_trader import (
    TraderClientObject,
    BadRequestError,
    Unauthorized,
    NoBuyOrders,
    InventoryItem,
    BuyOrder,
    Discount,
    OperationsHistoryItem,
    WebSocketMessage
)

if TYPE_CHECKING:
    from steam_trader import Client

@dataclass
class WSToken(TraderClientObject):
    """Класс, представляющий WS токен. Незадокументированно.

    Attributes:
        steam_id: (:obj:`str`)
        time: (:obj:`int`)
        hash: (:obj:`str`)
        client (:obj:`Client` optional): Клиент Steam Trader.
    """

    steam_id: str
    time: int
    hash: str
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['WSToken']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.WSToken`: WS токен.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 401:
                    raise Unauthorized('Вы не зарегистрированны')

        data = super(WSToken, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class Inventory(TraderClientObject):
    """Класс, представляющий инвентарь клиента.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        count (:obj:`int`): Количество всех предметов в инвентаре Steam.
        game (:obj:`int`): ID игры к которой принадлежит инвентарь (Название не совпадает с документацией).
        last_update (:obj:`int`): Timestamp последнего обновления инвентаря.
        items (:Sequence:`steam_trader.InventoryItem`): Последовательность с предметами в инвентаре.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    count: int
    game: int
    last_update: int
    items: Sequence['InventoryItem']
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['Inventory']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.Inventory`: Инвентарь клиента.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            try:
                match data['code']:
                    case 400:
                        raise BadRequestError('Неправильный запрос')
                    case 401:
                        raise Unauthorized('Неправильный api-токен')
            except KeyError:
                pass

        for i, offer in enumerate(data['items']):
            data['items'][i] = InventoryItem.de_json(offer)

        data = super(Inventory, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class BuyOrders(TraderClientObject):
    """Класс, представляющий ваши запросы на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (:Sequence:`steam_trader.BuyOrder`): Последовательность запросов на покупку.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """
    success: bool
    data: Sequence['BuyOrder']
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['BuyOrders']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyOrders`, optional: Ваши запросы на покупку.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Неправильный api-токен')
                case 1:
                    raise NoBuyOrders('Нет запросов на покупку')

        for i, offer in enumerate(data['data']):
            data['data'][i] = BuyOrder.de_json(offer)

        data = super(BuyOrders, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class Discounts(TraderClientObject):
    """Класс, представляющий комиссии/скидки на игры, доступные на сайте.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (:dict:`int, steam_trader.Discount`): Словарь, содержащий комисии/скидки.
        client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    data: Dict[int, Discount]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['Discounts']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.Discounts, optional`: Комиссии/скидки на игры.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Неправильный api-токен')

        # Конвертируем ключ в число для совместимости с константами
        new_data = {int(appid): Discount.de_json(_dict) for appid, _dict in data['data'].items()}
        data['data'] = new_data
        data = super(Discounts, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class OperationsHistory(TraderClientObject):
    """Класс, представляющий истории операций, произведённых на сайте.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        data (:Sequence:`steam_trader.OperationsHistoryItem`): Последовательность историй операций
        client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    data: Sequence[OperationsHistoryItem]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['OperationsHistory']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.Discounts`, optional: Истории операций.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Неправильный api-токен')

        # Конвертируем ключ в число для совместимости с константами
        for i, item in enumerate(data['data']):
            data['data'][i] = OperationsHistoryItem.de_json(item)

        data = super(OperationsHistory, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class InventoryState(TraderClientObject):
    """Класс, представляющий текущий статус обновления инвентаря.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        updating_now (:obj:`bool`): Инвентарь обновляется в данный момент.
        last_update (:obj:`int`): Timestamp, когда последний раз был обновлён инвентарь
        items_in_cache (:obj:`int`): Количество предметов в инвентаре.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    updating_now: bool
    last_update: int
    items_in_cache: int
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['InventoryState']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.InventoryState`, optional: Текущий статус обновления инвентаря.
        """

        if not cls.is_valid_model_data(data):
            return None

        data.update({  # перенос с camleCase на snake_case
            'updating_now': data['updatingNow'],
            'last_update': data['lastUpdate'],
            'items_in_cache': data['itemsInCache']
        })

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Неправильный api-токен')

        data = super(InventoryState, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class AltWebSocket(TraderClientObject):
    """Класс, представляющий запрос альтернативным WebSocket.

    Attributes:
        success (:obj:`bool`): Результат запроса. Если false, сообщений в поле messages не будет, при этом соединение будет поддержано.
        messages (:Sequence:`steam_trader.WebSocketMessage`): Последовательность с WebSocket сообщениями.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    messages: Sequence[WebSocketMessage]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['AltWebSocket']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.AltWebSocket`: Запрос альтернативным WebSocket.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            return

        for i, message in enumerate(data['messages']):
            data['messages'][i] = BuyOrder.de_json(message)

        data = super(WebSocketMessage, cls).de_json(data, client)

        return cls(client=client, **data)
