from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from steam_trader import TraderClientObject

if TYPE_CHECKING:
    from steam_trader import Client

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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['SellHistoryItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ItemInfo`: Информация о предмете.
        """

        new_data = {'date': data[0], 'price': data[1]}

        data = super(SellHistoryItem, cls).de_json(new_data)

        return cls(**data)

@dataclass
class InventoryItem(TraderClientObject):
    """Класс, представляющий предмет в инвентаре.

    Attributes:
        id (:obj:`bool`, optional): ID заявки на покупку/продажу. Может быть пустым.
        assetid (:obj:`int`, optional): AssetID предмета в Steam. Может быть пустым.
        gid (:obj:`int`): ID группы предметов.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`, optional): Цена, за которую предмет был выставлен/куплен/продан предмет без учета скидки/комиссии. Может быть пустым.
        currency (:obj:`int`, optional): Валюта, за которую предмет был выставлен/куплен/продан. Значение 1 - рубль. Может быть пустым.
        timer (:obj:`int`, optional): Время, которое доступно для приема/передачи этого предмета. Может быть пустым.
        type (:obj:`int`, optional): Тип предмета. 0 - продажа, 1 - покупка. Может быть пустым.
        status (:obj:`int`): Статус предмета.
           -2	Предмет в инвентаре Steam не выставлен на продажу.
            0	Предмет выставлен на продажу или выставлена заявка на покупку. Для различия используется поле type.
            1	Предмет был куплен/продан и ожидает передачи боту или P2P способом. Для различия используется поле type.
            2	Предмет был передан боту или P2P способом и ожидает приёма покупателем.
            6	Предмет находится в режиме резервного времени. На сайте отображается как "Проверяется" после истечения времени на передачу боту или P2P способом.
        position (:obj:`int`, optional): Позиция предмета в списке заявок на покупку/продажу. Может быть пустым.
        nc (:obj:`int`, optional): ID заявки на продажу для бескомиссионной ссылки. Может быть пустым.
        percent (:obj:`float`, optional): Размер скидки/комиссии в процентах, с которой был куплен/продан предмет. Может быть пустым.
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['InventoryItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ItemInfo`: Информация о предмете.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(InventoryItem, cls).de_json(data)

        return cls(**data)

@dataclass
class BuyOrder(TraderClientObject):
    """Класс, представляющий информацию о запросе на покупку.

    Attributes:
        id (:obj:`bool`, optional): ID заявки на покупку.
        gid (:obj:`int`): ID группы предметов.
        gameid (:obj:`int`): AppID приложения в Steam
        hash_name (:obj:`str`): Параметр market_hash_name в Steam
        date (:obj:`int`): Timestamp подачи заявки
        price (:obj:`float`): Предлагаемая цена покупки без учета скидки
        currency (:obj:`int`): Валюта, значение 1 - рубль
        position (:obj:`int`): Позиция заявки в очереди
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['BuyOrder']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyOrder`: Информация о запрос на покупку.
        """

        if not cls.is_valid_model_data(data):
            return None

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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['Discount']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.Discount`: Информацию о комиссии/скидке в определённой игре.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(Discount, cls).de_json(data)

        return cls(**data)

@dataclass
class OperationsHistoryItem(TraderClientObject):
    """Класс, представляющий информацию о предмете в истории операций.

    Attributes:
        id (:obj:`int`): ID Операции.
        name (:obj:`str`): Название операции.
        type (:obj:`int`): Тип операции.
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['OperationsHistoryItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.OperationsHistoryItem`: Информацию о предмете в истории операций.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(OperationsHistoryItem, cls).de_json(data)

        return cls(**data)

@dataclass
class WebSocketMessage(TraderClientObject):
    """Класс, представляющий AltWebSsocket сообщение.

    Attributes:
        type (:obj:`int`): Тип WebSocket сообщения в десятичном виде.
        data (:obj:`str`): WebSocket сообщение.
    """

    type: int
    data: str

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['WebSocketMessage']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.WebSocketMessage`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.Discount`: Комиссия/скидка.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(WebSocketMessage, cls).de_json(data)

        return cls(**data)

@dataclass
class MultiBuyOrder(TraderClientObject):
    """Класс, представляющий информацию о запросе из steam_clieant.MultiBuyInfo

    Args:
        id (:obj:`int`): ID заявки.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`): Цена, за которую был куплен предмет с уёетом скидки.
    """

    id: int
    itemid: int
    price: float

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['MultiBuyOrder']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.MultiBuyOrder`: Информация о запросе из steam_clieant.MultiBuyInfo
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(MultiBuyOrder, cls).de_json(data)

        return cls(**data)

@dataclass
class ItemForExchange(TraderClientObject):
    """Класс, представляющий информацию о предмете для передачи/получения боту.

    Attributes:
        id (:obj:`bool`): ID покупки/продажи.
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
        steam_item (:obj:`bool`): Если присутствует этот параметр и имеет значение false, значит этот предмет отсутствует в вашем инвентаре Steam
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['ItemForExchange']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ItemForExchange`: Информация о предмете для передачи/получения.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(ItemForExchange, cls).de_json(data)

        return cls(**data)

@dataclass
class TradeDescription(TraderClientObject):
    """Класс, предстваляющий описание предмета для передачи/получения боту.

    Attributes:
        type: (:obj:`str`): Тип предмета.
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['TradeDescription']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.TradeDescription`: Описание предмета для передачи/получения боту.
        """

        if not cls.is_valid_model_data(data):
            return None

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
        itemid (:obj:`int`): ID предмета в нашей базе.
        gid (:obj:`int`): Идентификатор группы предметов в нашей базе.
        price (:obj:`int`): Цена, за которую предмет был куплен/продан с учетом скидки/комиссии.
        currency (:obj:`int`): Валюта покупки/продажи.
        percent (:obj:`float`): Размер скидки/комиссии в процентах, с которой был куплен/продан предмет.
    """

    id: int
    assetid: int
    gameid: int
    contextid: int
    classid: int
    instanceid: int
    itemid: int
    gid: int
    price: float
    currency: int
    percent: float

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['ExchangeItem']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ExchangeItem`: Предмет, на который был отправлен обмен.
        """

        if not cls.is_valid_model_data(data):
            return None

        data = super(ExchangeItem, cls).de_json(data)

        return cls(**data)
