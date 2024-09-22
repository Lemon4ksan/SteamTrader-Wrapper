from dataclasses import dataclass
from typing import TYPE_CHECKING, Union

from ._base import TraderClientObject

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class SellOffer(TraderClientObject):
    """Класс, представляющий информацию о предложении продажи.

    Attributes:
        id (:obj:`int`): Уникальный ID заявки.
        classid (:obj:`int`): ClassID предмета в Steam.
        instanceid (:obj:`int`): InstanceID предмета в Steam.
        itemid (:obj:`int`): ID предмета.
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
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'SellOffer':

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
    def de_json(
            cls: dataclass,
            data: dict,
            client: Union['Client', 'ClientAsync', None] = None
    ) -> 'BuyOffer':

        data = super(BuyOffer, cls).de_json(data)

        return cls(**data)
