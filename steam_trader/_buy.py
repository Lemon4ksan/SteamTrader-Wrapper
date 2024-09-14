import logging
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
        gid (:obj:`int`): ID группы предметов.
        itemid (:obj:`int`): Униклаьный ID купленного предмета.
        price (:obj:`float`): Цена, за которую был куплен предмет с учётом скидки.
        new_price (:obj:`float`): Новая цена лучшего предложения о продаже для варианта покупки Commodity,
            если у группы предметов ещё имеются предложения о продаже. Для остальных вариантов покупки будет 0
        discount (:obj:`float`): Размер скидки в процентах, за которую был куплен предмет.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    id: int
    gid: int
    itemid: int
    price: float
    new_price: float
    discount: float
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'BuyResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`: Купленный предмет.
        """

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 429:
                    raise exceptions.TooManyRequests('Вы отправили слишком много запросов.')
                case 1:
                    raise exceptions.InternalError('При создании запроса произошла неизвестная ошибка.')
                case 3:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 4:
                    raise exceptions.NoLongerExists('Предложение больше недействительно.')
                case 5:
                    raise exceptions.NotEnoughMoney('Недостаточно средств.')

        data = super(BuyResult, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class BuyOrderResult(TraderClientObject):
    """Класс, представляющий результат запроса на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        executed (:obj:`int`): Количество исполненных заявок.
        placed (:obj:`int`): Количество размещённых на маркет заявок.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    executed: int
    placed: int
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'BuyOrderResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`: Результат запроса на покупку.
        """

        del data['orders']  # Конфликт с steam_trader.BuyOrder

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 429:
                    raise exceptions.TooManyRequests('Вы отправили слишком много запросов.')
                case 1:
                    raise exceptions.InternalError('При создании запроса произошла неизвестная ошибка.')
                case 2:
                    raise exceptions.UnknownItem('Неизвестный предмет.')
                case 3:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 4:
                    raise exceptions.NoLongerExists('Предложение больше недействительно.')
                case 5:
                    raise exceptions.NotEnoughMoney('Недостаточно средств.')

        data = super(BuyOrderResult, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class MultiBuyResult(TraderClientObject):
    """Класс, представляющий результат мульти-покупки.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        balance (:obj:`float`, optional): Баланс после покупки предметов. Указывается если success = True
        spent (:obj:`float`, optional): Сумма потраченных средств на покупку предметов. Указывается если success = True
        orders (Sequence[:class:`steam_trader.MultiBuyOrder`], optional):
            Последовательность купленных предметов. Указывается если success = True
        left (:obj:`int`): Сколько предметов по этой цене осталось. Если операция прошла успешно, всегда равен 0.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.

    Changes:
        0.2.3: Теперь, если во время операции закончиться баланс, вместо ошибки,
            в датаклассе будет указано кол-во оставшихся предметов по данной цене.
    """

    success: bool
    client: Union['Client', 'ClientAsync', None]
    balance: Optional[float] = None
    spent: Optional[float] = None
    orders: Optional[Sequence['MultiBuyOrder']] = None
    left: int = 0

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'MultiBuyResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.BuyResult`: Результат мульти-покупки.
        """

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос.')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен.')
                case 429:
                    raise exceptions.TooManyRequests('Вы отправили слишком много запросов.')
                case 1:
                    raise exceptions.InternalError('При создании запроса произошла неизвестная ошибка.')
                case 2:
                    logging.warning(data['error'])
                case 3:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 5:
                    raise exceptions.NotEnoughMoney('Недостаточно средств.')

        for i, offer in enumerate(data['orders']):
            data['orders'][i] = MultiBuyOrder.de_json(offer)

        data = super(MultiBuyResult, cls).de_json(data)

        return cls(client=client, **data)
