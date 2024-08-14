from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence, List

from steam_trader import (
    TraderClientObject,
    BadRequestError,
    Unauthorized,
    UnknownItem,
    InternalError,
    SellOffer,
    BuyOffer,
    SellHistoryItem
)

if TYPE_CHECKING:
    from steam_trader import Client

@dataclass
class MinPrices(TraderClientObject):
    """Класс, представляющий минимальную/максимальную цену на предмет.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        market_price (:obj:`float`, optional): Минимальная цена продажи. Может быть пустым.
        buy_price (:obj:`float`, optional): Максимальная цена покупки. Может быть пустым.
        steam_price (:obj:`float`, optional): Минимальная цена в Steam. Может быть пустым.
        count_sell_offers (:obj:`int`): Количество предложений о продаже.
        count_buy_offers (:obj:`int`): Количество предложений о покупке.
        client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    market_price: Optional[float]
    buy_price: Optional[float]
    steam_price: Optional[float]
    count_sell_offers: int
    count_buy_offers: int
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['MinPrices']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.MinPrices`, optional: Минимальная/максимальная цена на предмет.
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
                    raise InternalError('При выполнении запроса произошла ошибка')
                case 2:
                    raise UnknownItem('Неизвестный предмет')

        data = super(MinPrices, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class ItemInfo(TraderClientObject):
    # TODO: Добавить датакласс для фильтра
    """Класс, представляющий группу предметов на сайте.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        name (:obj:`str`): Локализованное (переведённое) название предмета.
        hash_name (:obj:`str`): Параметр 'market_hash_name' в Steam.
        type (:obj:`str`): Тип предмета (из Steam).
        gameid (:obj:`int`): AppID приложения в Steam.
        contextid (:obj:`int`): ContextID приложения в Steam.
        color (:obj:`str`): Hex код цвета предмета (из Steam).
        small_image (:obj:`str`): Абсолютная ссылка на маленькое изображение предмета.
        large_image (:obj:`str`): Абсолютная ссылка на большое изображение предмета.
        marketable (:obj:`bool`): Параметр 'marketable' в Steam.
        tradable (:obj:`bool`): Параметр 'tradable' в Steam.
        description (:obj:`str`): Локализованное (переведённое) описание предмета.
        market_price (:obj:`float`, optional): Минимальная цена продажи. Может быть пустым.
        buy_price (:obj:`float`, optional): Максимальная цена покупки. Может быть пустым.
        steam_price (:obj:`float`, optional): Минимальная цена в Steam. Может быть пустым.
        filters (:obj:`dict`): Фильтры, используемые для поиска на сайте (нет в документации).
        sell_offers (:Sequnce:`steam_trader.SellOffer`): Последовательность с предложениями о продаже.
        buy_offers (:Sequnce:`steam_trader.BuyOffer`): Последовательность с предложениями о покупке.
        sell_history (:Sequence:`steam_trader.SellHistoryItem`): Последовательность, содержащая историю продаж.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    name: str
    hash_name: str
    type: str
    gameid: int
    contextid: int
    color: str
    small_image: str
    large_image: str
    marketable: bool
    tradable: bool
    description: str
    market_price: Optional[float]
    buy_price: Optional[float]
    steam_price: Optional[float]
    filters: dict
    sell_offers: Sequence['SellOffer']
    buy_offers: Sequence['BuyOffer']
    sell_history: list
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['ItemInfo']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ItemInfo`, optional: Группа предметов на сайте.
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
                    raise InternalError('При выполнении запроса произошла ошибка')
                case 2:
                    raise UnknownItem('Неизвестный предмет')

        for i, offer in enumerate(data['sell_offers']):
            data['sell_offers'][i] = SellOffer.de_json(offer)

        for i, offer in enumerate(data['buy_offers']):
            data['buy_offers'][i] = BuyOffer.de_json(offer)

        for i, item in enumerate(data['sell_history']):
            data['sell_history'][i] = SellHistoryItem.de_json(item)

        data = super(ItemInfo, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class OrderBook(TraderClientObject):
    """Класс, представляющий заявоки о покупке/продаже предмета.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        sell (:Sequence:`list[int, int]`): Сгруппированный по цене список заявок на продажу. Каждый элемент в списке является массивом, где первый элемент - это цена, а второй - количество заявок.
        buy (:Sequence:`list[int, int]`): Сгруппированный по цене список заявок на покупку. Каждый элемент в списке является массивом, где первый элемент - это цена, а второй - количество заявок.
        total_sell (:obj:`int`): Количество всех заявок на продажу.
        total_buy (:obj:`int`): Количество всех заявок на покупку.
        client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    sell: Sequence[List[int]]
    buy: Sequence[List[int]]
    total_sell: int
    total_buy: int
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['OrderBook']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.OrderBook`: Список заявок о покупке/продаже предмета.
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
                    raise InternalError('При выполнении запроса произошла ошибка')

        data = super(OrderBook, cls).de_json(data, client)

        return cls(client=client, **data)
