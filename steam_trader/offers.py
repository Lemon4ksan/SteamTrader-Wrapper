from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from steam_trader import TraderClientObject

if TYPE_CHECKING:
    from steam_trader import Client

@dataclass
class SellOffer(TraderClientObject):
    """Класс, представляющий информацию о предложении продажи.

    Attributes:
        id (:obj:`int`): ID заявки.
        classid (:obj:`int`): ClassID предмета в Steam.
        instanceid (:obj:`int`): InstanceID предмета в Steam.
        itemid (:obj:`int`): Уникальный ID предмета.
        price (:obj:`float`): Цена предложения о покупке/продаже.
        currency (:obj:`int`): Валюта покупки/продажи.
    """

    id: int
    classid: int
    instanceid: int
    itemid: int
    price: float
    currency: int

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['SellOffer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.SellOffer`, optional: Информация о предложении продажи.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(SellOffer, cls).de_json(data)

        return cls(**data)

@dataclass
class BuyOffer(TraderClientObject):
    """Класс, представляющий информацию о запросе на покупку.

    Attributes:
        id (:obj:`int`): ID заявки.
        price (:obj:`float`): Цена предложения о покупке/продаже.
        currency (:obj:`int`): Валюта покупки/продажи.
    """

    id: int
    price: float
    currency: int

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['BuyOffer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyOffer`, optional: Информация о запросе на покупку.
        """
        if not cls.is_valid_model_data(data):
            return None

        data = super(BuyOffer, cls).de_json(data)

        return cls(**data)

