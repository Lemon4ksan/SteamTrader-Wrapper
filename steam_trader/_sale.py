from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from steam_trader import exceptions
from ._base import TraderClientObject

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class SellResult(TraderClientObject):
    """Класс, представляющий информацию о выставленном на продажу предмете.

     Attributes:
         success (:obj:`bool`): Результат запроса.
         id: (:obj:`int`): ID продажи.
         position (:obj:`int`): Позиция предмета в очереди.
         fast_execute (:obj:`bool`): Был ли предмет продан моментально.
         nc (:obj:`str`): Идентификатор для бескомиссионной продажи предмета.
         price (:obj:`float`, optional): Цена, за которую был продан предмет с учетом комиссии.
            Указывается, если 'fast_execute' = True
         commission (:obj:`float`, optional): Размер комиссии в процентах, за которую был продан предмет.
            Указывается, если 'fast_execute' = True
         client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
     """

    success: bool
    id: int
    position: int
    fast_execute: bool
    nc: str
    client: Union['Client', 'ClientAsync', None]
    price: Optional[float] = None
    commission: Optional[float] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'SellResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.SellResult`: Информация о выставлении предмета на продажу.
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
                    raise exceptions.UnknownItem('Неизвестный предмет.')
                case 3:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 4:
                    raise exceptions.IncorrectPrice(data['error'])
                case 5:
                    raise exceptions.ItemAlreadySold('Предмет уже продан или отстутствует.')
                case 6:
                    raise exceptions.AuthenticatorError('Мобильный аутентификатор не подключён или с момента его подключения ещё не прошло 7 дней.')

        data = super(SellResult, cls).de_json(data)

        return cls(client=client, **data)
