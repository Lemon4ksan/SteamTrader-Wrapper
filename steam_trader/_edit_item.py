from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Sequence

from steam_trader import exceptions
from ._base import TraderClientObject

if TYPE_CHECKING:
    from steam_trader import Client
    from ._client_async import ClientAsync

@dataclass
class EditPriceResult(TraderClientObject):
    """Класс, представляющий результат запроса на изменение цены.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        type (:obj:`int`): Тип заявки. 0 - продажа, 1 - покупка.
        position (:obj:`int`): Позиция предмета в очереди.
        fast_execute (:obj:`bool`): Был ли предмет продан/куплен моментально.
        new_id (:obj:`int`, optional): Новый ID заявки. Указывается, если 'fast_execute' = true.
            Новый ID присваивается только заявкам на ПОКУПКУ и только в случае редактирования уже имеющейся заявки.
        price (:obj:`float`, optional): Цена, за которую был продан/куплен предмет с учётом комиссии/скидки.
            Указывается, если 'fast_execute' = true.
        percent (:obj:`float`, optional): Размер комиссии/скидки в процентах, за которую был продан/куплен предмет.
            Указывается, если 'fast_execute' = true.
        client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    type: int
    position: int
    fast_execute: bool
    new_id: Optional[int] = None
    price: Optional[float] = None
    percent: Optional[float] = None
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] | Optional['ClientAsync'] = None) -> Optional['EditPriceResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.EditPriceResult`, optional: Результат запроса на изменение цены.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен')
                case 1:
                    raise exceptions.InternalError('Ошибка редактирования предмета.')
                case 2:
                    raise exceptions.NotFoundError('У вас нет данного предмета или он уже продан.')
                case 4:
                    raise exceptions.IncorrectPrice(data['error'])
                case 5:
                    raise exceptions.NotEnoughMoney('Для покупки не достаточно средств.')

        data = super(EditPriceResult, cls).de_json(data, client)

        return cls(**data)

@dataclass
class DeleteItemResult(TraderClientObject):
    """Класс, представляющий результат запроса снятия предмета с продажи/заявки на покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        has_ex (:obj:`bool`): Есть ли доступный обмен на сайте.
        has_bot_ex (:obj:`bool`): Есть ли доступный обмен с ботом.
        has_p2p_ex (:obj:`bool`): Есть ли доступный P2P обмен.
        total_fines (:obj:`int`): Общее количество штрафных баллов.
        fine_date (:obj:`int`, optional): Дата снятия штрафных баллов. Если None - штрафных баллов нет.
        client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    has_ex: bool
    has_bot_ex: bool
    has_p2p_ex: bool
    total_fines: int
    fine_date: Optional[int]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] | Optional['ClientAsync'] = None) -> Optional['DeleteItemResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.DeleteItemResult`, optional: Результат запроса снятия предмета с продажи/заявки на покупку.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен')
                case 1:
                    raise exceptions.InternalError('Ошибка редактирования предмета.')
                case 2:
                    raise exceptions.UnknownItem('	Неизвестный предмет.')

        data = super(DeleteItemResult, cls).de_json(data, client)

        return cls(**data)

@dataclass
class GetDownOrdersResult(TraderClientObject):
    """Класс, представляющий результат снятия всех заявок на продажу/покупку.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        count (:obj:`int`): Количество удалённых предложений.
        ids (Sequence[:obj:`int`]): Список из ID удалённых предложений.
        client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.
    """

    success: bool
    count: int
    ids: Sequence[int]
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] | Optional['ClientAsync'] = None) -> Optional['GetDownOrdersResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.EditPriceResult`, optional: Результат запроса на изменение цены.
        """

        if not cls.is_valid_model_data(data):
            return

        if not data['success']:
            match data['code']:
                case 400:
                    raise exceptions.BadRequestError('Неправильный запрос')
                case 401:
                    raise exceptions.Unauthorized('Неправильный api-токен')
                case 1:
                    raise exceptions.InternalError('Ошибка редактирования предмета')
                case 2:
                    raise exceptions.NoTradeItems('Нет заявок на продажу/покупку')

        data = super(GetDownOrdersResult, cls).de_json(data, client)

        return cls(**data)
