from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

from steam_trader import (
    TraderClientObject,
    BadRequestError,
    Unauthorized,
    NoLongerExists,
    NoTradeLink,
    NotEnoughMoney,
    OfferCreationFail,
    UnknownItem,
    MultiBuyOrder
)

if TYPE_CHECKING:
    from steam_trader import Client

@dataclass
class BuyResult(TraderClientObject):
    """Класс, представляющий результат покупки.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        id (:obj:`int`): ID покупки.
        itemid (:obj:`int`): Униклаьный ID купленного предмета.
        price (:obj:`float`): Цена, за которую был куплен предмет с учётом скидки.
        new_price (:obj:`float`): Новая цена лучшего предложения о продаже для варианта покупки Commodity, если у группы предметов ещё имеются предложения о продаже. Для остальных вариантов покупки будет 0
        discount (:obj:`float`): Размер скидки в процентах, за которую был куплен предмет.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    id: int
    gid: int
    itemid: int
    price: float
    new_price: float
    discount: float
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['BuyResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyResult`: Купленный предмет.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Вы не зарегистрированны')
                case 1:
                    raise OfferCreationFail('Ошибка создания заявки.')
                case 3:
                    raise NoTradeLink('У Вас нет ссылки для обмена.')
                case 4:
                    raise NoLongerExists('Извините, данное предложение больше недействительно.')
                case 5:
                    raise NotEnoughMoney('Для покупки не достаточно средств.')

        data = super(BuyResult, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class BuyOrderResult(TraderClientObject):
    """Класс, представляющий результат запроса на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        executed (:obj:`int`): Количество исполненных заявок.
        placed (:obj:`int`): Количество размещённых на маркет заявок.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    executed: int
    placed: int
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['BuyOrderResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyResult`: Результат запроса на покупку.
        """

        if not cls.is_valid_model_data(data):
            return None

        del data['orders']  # Конфликт с steam_trader.BuyOrder

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Вы не зарегистрированны')
                case 1:
                    raise OfferCreationFail('Ошибка создания заявки.')
                case 2:
                    raise UnknownItem('Неизвестный предмет')
                case 3:
                    raise NoTradeLink('У Вас нет ссылки для обмена.')
                case 4:
                    raise NoLongerExists('Извините, данное предложение больше недействительно.')
                case 5:
                    raise NotEnoughMoney('Для покупки не достаточно средств.')

        data = super(BuyOrderResult, cls).de_json(data, client)

        return cls(client=client, **data)

@dataclass
class MultiBuyResult(TraderClientObject):
    """Класс, представляющий результат мульти-покупки.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        balance (:obj:`float`): Баланс после покупки предметов.
        spent (:obj:`float`): Сумма потраченных средств на покупку предметов.
        orders (:Sequence:`MultiBuyOrder`): Последовательность купленных предметов.
        client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    balance: float
    spent: float
    orders: Sequence['MultiBuyOrder']
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['MultiBuyResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.BuyResult`: Результат мульти-покупки.
        """

        if not cls.is_valid_model_data(data):
            return None

        if not data['success']:
            match data['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Вы не зарегистрированны')
                case 1:
                    raise OfferCreationFail('Ошибка создания заявки.')
                case 2:
                    raise NotEnoughMoney(data['error'])
                case 3:
                    raise NoTradeLink('У Вас нет ссылки для обмена.')
                case 5:
                    raise NotEnoughMoney('Для покупки не достаточно средств.')

        for i, offer in enumerate(data['orders']):
            data['orders'][i] = MultiBuyOrder.de_json(offer)

        data = super(MultiBuyResult, cls).de_json(data, client)

        return cls(client=client, **data)
