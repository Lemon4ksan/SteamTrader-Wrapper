from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from ._base import TraderClientObject

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class SellHistoryItem(TraderClientObject):
    """Класс, представляющий информацию о предмете в истории продаж.

    Attributes:
        date (:obj:`int`): Timestamp времени продажи.
        price (:obj:`float`): Цена предложения о покупке/продаже.
    """

    date: int
    price: float

    @classmethod
    def de_json(cls: dataclass, data: list, client: Union['Client', 'ClientAsync', None] = None) -> 'SellHistoryItem':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.SellHistoryItem`: Информация о предмете в истории продаж.
        """

        data = {'date': data[0], 'price': float(data[1])}  # Принудительно конвертируем для совместимости.

        return cls(**data)

@dataclass
class InventoryItem(TraderClientObject):
    """Класс, представляющий предмет в инвентаре.

    Attributes:
        id (:obj:`int`, optional): ID заявки на покупку/продажу. Может быть пустым.
        assetid (:obj:`int`, optional): AssetID предмета в Steam. Может быть пустым.
        gid (:obj:`int`): ID группы предметов.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`, optional): Цена, за которую предмет был выставлен/куплен/продан предмет без учёта
            скидки/комиссии. Может быть пустым.
        currency (:obj:`int`, optional): Валюта, за которую предмет был выставлен/куплен/продан. Значение 1 - рубль.
            Может быть пустым.
        timer (:obj:`int`, optional): Время, которое доступно для приема/передачи этого предмета. Может быть пустым.
        type (:obj:`int`, optional): Тип предмета. 0 - продажа, 1 - покупка. Может быть пустым.
        status (:obj:`int`): Статус предмета.
           -2 - Предмет в инвентаре Steam не выставлен на продажу.
            0 - Предмет выставлен на продажу или выставлена заявка на покупку. Для различия используется поле type.
            1 - Предмет был куплен/продан и ожидает передачи боту или P2P способом. Для различия используется поле type.
            2 - Предмет был передан боту или P2P способом и ожидает приёма покупателем.
            6 - Предмет находится в режиме резервного времени. На сайте отображается как "Проверяется"
                после истечения времени на передачу боту или P2P способом.
        position (:obj:`int`, optional): Позиция предмета в списке заявок на покупку/продажу. Может быть пустым.
        nc (:obj:`int`, optional): ID заявки на продажу для бескомиссионной ссылки. Может быть пустым.
        percent (:obj:`float`, optional): Размер скидки/комиссии в процентах, с которой был куплен/продан предмет.
            Может быть пустым.
        steam_item (:obj:`bool`): Флаг, определяющий, имеется ли этот предмет в инвентаре в Steam (для продавца).
        nm (:obj:`bool`): Незадокументированно.
    """

    id: Optional[int]
    assetid: Optional[int]
    gid: int
    itemid: int
    price: Optional[float]
    currency: Optional[int]
    timer: Optional[int]
    type: Optional[int]
    status: int
    position: Optional[int]
    nc: Optional[int]
    percent: Optional[float]
    steam_item: bool
    nm: bool

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'InventoryItem':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.InventoryItem`: Предмет в инвентаре.
        """

        data = super(InventoryItem, cls).de_json(data)

        return cls(**data)

@dataclass
class Filter(TraderClientObject):
    """Класс, представляющий фильтр.

    Attributes:
        id (:obj:`int`, optional): ID фильтра, может быть пустым. Если вы создаёте класс вручную,
            то обязательно укажите этот параметр.
        title (:obj:`str`, optional): Тайтл фильтра, может быть пустым.
        color (:obj:`str`, optionl): Hex цвет фильтра, может быть пустым.
    """

    id: Optional[int]
    title: Optional[str] = None
    color: Optional[str] = None

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'Filter':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Filter`, optional: Фильтр.
        """

        data = super(Filter, cls).de_json(data)

        return cls(**data)

@dataclass
class Filters(TraderClientObject):
    """Класс, представляющий фильтры, используемые для поиска на сайте.

    Attributes:
        quality (Sequence[:class:`steam_trader.Filter`], optional):
            Качество предмета (TF2, DOTA2).
        type (Sequence[:class:`steam_trader.Filter`], optional):
            Тип предмета (TF2, DOTA2).
        used_by (Sequence[:class:`steam_trader.Filter`], optional):
            Класс, который использует предмет (TF2).
        craft (Sequence[:class:`steam_trader.Filter`], optional):
            Информация о карфте (TF2).
        region (Sequence[:class:`steam_trader.Filter`], optional):
            Регион игры (SteamGift).
        genre (Sequence[:class:`steam_trader.Filter`], optional):
            Жанр игры (SteamGift).
        mode (Sequence[:class:`steam_trader.Filter`], optional):
            Тип игры, взаимодействие с Steam (SteamGift).
        trade (Sequence[:class:`steam_trader.Filter`], optional):
            Информация об обмене (SteamGift).
        rarity (Sequence[:class:`steam_trader.Filter`], optional):
            Редкость предмета (DOTA2).
        hero (Sequence[:class:`steam_trader.Filter`], optional):
            Герой, который использует предмет (DOTA2).
    """

    quality: Optional[Sequence['Filter']] = None
    type: Optional[Sequence['Filter']] = None
    used_by: Optional[Sequence['Filter']] = None
    craft: Optional[Sequence['Filter']] = None
    region: Optional[Sequence['Filter']] = None
    genre: Optional[Sequence['Filter']] = None
    mode: Optional[Sequence['Filter']] = None
    trade: Optional[Sequence['Filter']] = None
    rarity: Optional[Sequence['Filter']] = None
    hero: Optional[Sequence['Filter']] = None

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'Filters':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Filters`: Фильтры.
        """

        try:
            # TF2
            data.update({  # Затмевает встроенное имя class
                'used_by': data['class']
            })

            del data['class']

            for i, _filter in enumerate(data['quality']):
                data['quality'][i] = Filter.de_json(data['quality'][i])

            for i, _filter in enumerate(data['type']):
                data['type'][i] = Filter.de_json(data['type'][i])

            for i, _filter in enumerate(data['used_by']):
                data['used_by'][i] = Filter.de_json(data['used_by'][i])

            for i, _filter in enumerate(data['craft']):
                data['craft'][i] = Filter.de_json(data['craft'][i])

        except KeyError:
            try:
                # SteamGift
                for i, _filter in enumerate(data['region']):
                    data['region'][i] = Filter.de_json(data['region'][i])

                for i, _filter in enumerate(data['genre']):
                    data['genre'][i] = Filter.de_json(data['genre'][i])

                for i, _filter in enumerate(data['mode']):
                    data['mode'][i] = Filter.de_json(data['mode'][i])

                for i, _filter in enumerate(data['trade']):
                    data['trade'][i] = Filter.de_json(data['trade'][i])

            except KeyError:
                # DOTA2
                for i, _filter in enumerate(data['rarity']):
                    data['rarity'][i] = Filter.de_json(data['rarity'][i])

                for i, _filter in enumerate(data['quality']):
                    data['quality'][i] = Filter.de_json(data['quality'][i])

                for i, _filter in enumerate(data['type']):
                    data['type'][i] = Filter.de_json(data['type'][i])

                for i, _filter in enumerate(data['hero']):
                    data['hero'][i] = Filter.de_json(data['hero'][i])

        data = super(Filters, cls).de_json(data)

        return cls(**data)

@dataclass
class BuyOrder(TraderClientObject):
    """Класс, представляющий информацию о запросе на покупку.

    Attributes:
        id (:obj:`int`): ID заявки на покупку.
        gid (:obj:`int`): ID группы предметов.
        gameid (:obj:`int`): AppID приложения в Steam.
        hash_name (:obj:`str`): Параметр market_hash_name в Steam.
        date (:obj:`int`): Timestamp подачи заявки.
        price (:obj:`float`): Предлагаемая цена покупки без учёта скидки.
        currency (:obj:`int`): Валюта, значение 1 - рубль.
        position (:obj:`int`): Позиция заявки в очереди.
    """

    id: int
    gid: int
    gameid: int
    hash_name: str
    date: int
    price: float
    currency: int
    position: int

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'BuyOrder':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyOrder`: Информация о запрос на покупку.
        """

        data = super(BuyOrder, cls).de_json(data)

        return cls(**data)

@dataclass
class Discount(TraderClientObject):
    """Класс, представляющий информацию о комиссии/скидке в определённой игре.

    Attributes:
        total_buy (:obj:`float`): Cколько денег потрачено на покупки.
        total_sell (:obj:`float`): Cколько денег получено с продажи предметов.
        discount (:obj:`float`): Cкидка на покупку. Величина в %.
        commission (:obj:`float`): Комиссия на продажу. Величина в %.
    """

    total_buy: float
    total_sell: float
    discount: float
    commission: float

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'Discount':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Discount`: Информацию о комиссии/скидке в определённой игре.
        """

        data = super(Discount, cls).de_json(data)

        return cls(**data)

@dataclass
class OperationsHistoryItem(TraderClientObject):
    """Класс, представляющий информацию о предмете в истории операций.

    Attributes:
        id (:obj:`int`): ID Операции.
        name (:obj:`str`): Название операции.
        type (:obj:`int`): Тип операции. 0 - продажа, 1 - покупка.
        amount (:obj:`float`): Сумма операции.
        currency (:obj:`int`): Валюта, значение 1 - рубль.
        date (:obj:`int`): Timestamp операции.
    """

    id: int
    name: str
    type: int
    amount: float
    currency: int
    date: int

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'OperationsHistoryItem':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.OperationsHistoryItem`: Информацию о предмете в истории операций.
        """

        data = super(OperationsHistoryItem, cls).de_json(data)

        return cls(**data)

@dataclass
class AltWebSocketMessage(TraderClientObject):
    """Класс, представляющий AltWebSsocket сообщение.

    Attributes:
        type (:obj:`int`): Тип WebSocket сообщения в десятичном виде.
        data (:obj:`str`): WebSocket сообщение.
    """

    type: int
    data: str

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'AltWebSocketMessage':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.Discount`: Комиссия/скидка.
        """

        data = super(AltWebSocketMessage, cls).de_json(data)

        return cls(**data)

@dataclass
class MultiBuyOrder(TraderClientObject):
    """Класс, представляющий предмет из запроса на мульти-покупку.

    Args:
        id (:obj:`int`): ID заявки.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`): Цена, за которую был куплен предмет с учётом скидки.
    """

    id: int
    itemid: int
    price: float

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'MultiBuyOrder':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.MultiBuyOrder`: Запрос на покупку из steam_clieant.MultiBuyInfo.
        """

        data = super(MultiBuyOrder, cls).de_json(data)

        return cls(**data)

@dataclass
class ItemForExchange(TraderClientObject):
    """Класс, представляющий информацию о предмете для передачи/получения боту.

    Attributes:
        id (:obj:`int`): ID покупки/продажи.
        assetid (:obj:`int`): AssetID предмета в Steam.
        gameid (:obj:`int`): AppID приложения в Steam.
        contextid (:obj:`int`): ContextID приложения в Steam.
        classid (:obj:`int`): Параметр ClassID в Steam.
        instanceid (:obj:`int`): Параметр InstanceID в Steam.
        gid (:obj:`int`): ID группы предметов.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`): Цена предмета, за которую купили/продали, без учета комиссии/скидки.
        currency (:obj:`int`): Валюта покупки/продажи.
        timer (:obj:`int`): Cколько времени осталось до передачи боту/окончания гарантии.
        asset_type (:obj:`int`): Значение 0 - этот предмет для передачи боту. Значение 1 - для приёма предмета от бота.
        percent (:obj:`float`): Размер комиссии/скидки в процентах, за которую был продан/куплен предмет.
        steam_item (:obj:`bool`): Присутствует ли предмет в вашем инвентаре Steam.
    """

    id: int
    assetid: int
    gameid: int
    contextid: int
    classid: int
    instanceid: int
    gid: int
    itemid: int
    price: float
    currency: int
    timer: int
    asset_type: int
    percent: float
    steam_item: bool

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'ItemForExchange':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.ItemForExchange`: Информация о предмете для передачи/получения.
        """

        data = super(ItemForExchange, cls).de_json(data)

        return cls(**data)

@dataclass
class TradeDescription(TraderClientObject):
    """Класс, предстваляющий описание предмета для передачи/получения боту.

    Attributes:
        type (:obj:`str`): Тип предмета.
        description (:obj:`str`): Описание предмета.
        hash_name (:obj:`str`): Параметр market_hash_name в Steam.
        name (:obj:`str`): Локализованное (переведённое) название предмета.
        image_small (:obj:`str`): Маленькое изображение предмета.
        color (:obj:`str`): Цвет предмета (из Steam).
        outline (:obj:`str`): Цвет фильтра предмета (из Steam).
        gameid (:obj:`int`): AppID приложения в Steam
    """

    type: str
    description: str
    hash_name: str
    name: str
    image_small: str
    color: str
    outline: str
    gameid: int

    @classmethod
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'TradeDescription':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.TradeDescription`: Описание предмета для передачи/получения боту.
        """

        data = super(TradeDescription, cls).de_json(data)

        return cls(**data)

@dataclass
class ExchangeItem(TraderClientObject):
    """Класс, представляющий предмет, на который был отправлен обмен.

    Attributes:
        id (:obj:`int`): ID покупки/продажи.
        assetid (:obj:`int`): AssetID предмета в Steam.
        gameid (:obj:`int`): AppID приложения в Steam.
        contextid (:obj:`int`): ContextID приложения в Steam.
        classid (:obj:`int`): ClassID предмета в Steam.
        instanceid (:obj:`int`): InstanceID предмета в Steam.
        type (:obj:`int`): Значение 0 - предмет для передачи боту, значение 1 - предмет для приема от бота.
        itemid (:obj:`int`): ID предмета в нашей базе.
        gid (:obj:`int`): Идентификатор группы предметов в нашей базе.
        price (:obj:`int`): Цена, за которую предмет был куплен/продан с учётом скидки/комиссии.
        currency (:obj:`int`): Валюта покупки/продажи.
        percent (:obj:`float`): Размер скидки/комиссии в процентах, с которой был куплен/продан предмет.
    """

    id: int
    assetid: int
    gameid: int
    contextid: int
    classid: int
    instanceid: int
    type: int
    itemid: int
    gid: int
    price: float
    currency: int
    percent: float

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'ExchangeItem':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.ExchangeItem`: Предмет, на который был отправлен обмен.
        """

        data = super(ExchangeItem, cls).de_json(data)

        return cls(**data)
