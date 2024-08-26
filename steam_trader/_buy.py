from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from steam_trader import exceptions
from ._misc import MultiBuyOrder
from ._base import TraderClientObject

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class BuyResult(TraderClientObject):
    """Класс, представляющий результат покупки.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        id (:obj:`int`): ID покупки.
        itemid (:obj:`int`): Униклаьный ID купленного предмета.
        price (:obj:`float`): Цена, за которую был куплен предмет с учётом скидки.
        new_price (:obj:`float`): Новая цена лучшего предложения о продаже для варианта покупки Commodity,
            если у группы предметов ещё имеются предложения о продаже. Для остальных вариантов покупки будет 0
        discount (:obj:`float`): Размер скидки в процентах, за которую был куплен предмет.
        client (:class:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    id: int
    gid: int
    itemid: int
    price: float
    new_price: float
    discount: float
    client: Optional['Client']

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['BuyResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`, optional: Купленный предмет.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 1:
                    raise exceptions.OfferCreationFail('Ошибка создания заявки.')
                case 3:
                    raise exceptions.NoTradeLink('У Вас нет ссылки для обмена.')
                case 4:
                    raise exceptions.NoLongerExists('Извините, данное предложение больше недействительно.')
                case 5:
                    raise exceptions.NotEnoughMoney('Для покупки недостаточно средств.')

        data = super(BuyResult, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class BuyOrderResult(TraderClientObject):
    """Класс, представляющий результат запроса на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        executed (:obj:`int`): Количество исполненных заявок.
        placed (:obj:`int`): Количество размещённых на маркет заявок.
        client (:class:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    executed: int
    placed: int
    client: Optional['Client']

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['BuyOrderResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`, optional: Результат запроса на покупку.
        """

        if not cls.is_valid_model_data(data):
            return

        del data['orders']  # Конфликт с steam_trader.BuyOrder

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 1:
                    raise exceptions.OfferCreationFail('Ошибка создания заявки.')
                case 2:
                    raise exceptions.UnknownItem('Неизвестный предмет.')
                case 3:
                    raise exceptions.NoTradeLink('У Вас нет ссылки для обмена.')
                case 4:
                    raise exceptions.NoLongerExists('Данное предложение больше недействительно.')
                case 5:
                    raise exceptions.NotEnoughMoney('Для покупки недостаточно средств.')

        data = super(BuyOrderResult, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class MultiBuyResult(TraderClientObject):
    """Класс, представляющий результат мульти-покупки.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        balance (:obj:`float`): Баланс после покупки предметов.
        spent (:obj:`float`): Сумма потраченных средств на покупку предметов.
        orders (Sequence[:class:`steam_trader.MultiBuyOrder`, optional]): Последовательность купленных предметов.
        client (:class:`steam_trader.Client` optional): Клиент Steam Trader.
    """

    success: bool
    balance: float
    spent: float
    orders: Sequence[Optional['MultiBuyOrder']]
    client: Optional['Client']

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['MultiBuyResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`: Результат мульти-покупки.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 1:
                    raise exceptions.OfferCreationFail('Ошибка создания заявки.')
                case 2:
                    raise exceptions.NotEnoughMoney(data['error'])
                case 3:
                    raise exceptions.NoTradeLink('У Вас нет ссылки для обмена.')
                case 5:
                    raise exceptions.NotEnoughMoney('Для покупки не достаточно средств.')

        for i, offer in enumerate(data['orders']):
            data['orders'][i] = MultiBuyOrder.de_json(offer)

        data = super(MultiBuyResult, cls).de_json(data)

        return cls(client=client, **data)
