from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from steam_trader import (
    TraderClientObject,
    BadRequestError,
    Unauthorized,
    AuthenticatorError,
    UnknownItem,
    NoTradeLink,
    IncorrectPrice,
    ItemAlreadySold,
    OfferCreationFail
)

if TYPE_CHECKING:
    from steam_trader import Client

@dataclass
class ItemOnSale(TraderClientObject):
    """Класс, представляющий информацию о выставленном на продажу предмете.

     Attributes:
         success (:obj:`bool`): Результат запроса.
         id: (:obj:`int`): ID продажи.
         position (:obj:`int`): Позиция предмета в очереди.
         fast_execute (:obj:`bool`): Был ли предмет продан моментально.
         nc (:obj:`str`): Идентификатор для бескомиссионной продажи предмета.
         price (:obj:`float`): Цена, за которую был продан предмет с учетом комиссии. Указывается, если 'fast_execute' = True
         commission (:obj:`float`): Размер комиссии в процентах, за которую был продан предмет. Указывается, если 'fast_execute' = True
         client (:obj:`steam_trader.Client` optional): Клиент Steam Trader.
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
    def de_json(cls: dataclass, data: dict, client: Optional['Client'] = None) -> Optional['ItemOnSale']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :obj:`steam_trader.ItemOnSale`: Информация о выставлении предмета на продажу.
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
                    raise UnknownItem('Неизвестный предмет.')
                case 3:
                    raise NoTradeLink('У Вас нет ссылки для обмена.')
                case 4:
                    raise IncorrectPrice(data['error'])
                case 5:
                    raise ItemAlreadySold('У вас нет данного предмета или он уже продан.')
                case 6:
                    raise AuthenticatorError('У вас не подключён мобильный аутентификатор или с момента его подключения ещё не прошло 7 дней.')

        data = super(ItemOnSale, cls).de_json(data, client)

        return cls(client=client, **data)
