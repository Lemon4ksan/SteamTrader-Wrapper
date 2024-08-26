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
         client (:class:`steam_trader.Client` optional): Клиент Steam Trader.
     """

    success: bool
    id: int
    position: int
    fast_execute: bool
    nc: str
    price: Optional[float] = None
    commission: Optional[float] = None
    client: Optional['Client'] = None

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['SellResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.SellResult`, optional: Информация о выставлении предмета на продажу.
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
                    raise exceptions.UnknownItem('Неизвестный предмет.')
                case 3:
                    raise exceptions.NoTradeLink('У вас нет ссылки для обмена.')
                case 4:
                    raise exceptions.IncorrectPrice(data['error'])
                case 5:
                    raise exceptions.ItemAlreadySold('У вас нет данного предмета или он уже продан.')
                case 6:
                    raise exceptions.AuthenticatorError('У вас не подключён мобильный аутентификатор или с момента его подключения ещё не прошло 7 дней.')

        data = super(SellResult, cls).de_json(data)

        return cls(client=client, **data)
