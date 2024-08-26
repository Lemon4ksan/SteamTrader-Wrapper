from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from ._base import TraderClientObject
from ._misc import ExchangeItem

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class P2PTradeOffer(TraderClientObject):
    """Класс, представляющий данные для совершения p2p трейда. Незадокументированно.

    Attributes:
        sessionid (:obj:`str`):
        serverid (:obj:`int`):
        partner (:obj:`str`):
        tradeoffermessage (:obj:`str`):
        json_tradeoffer (:obj:`str`):
        captcha (:obj:`str`):
        trade_offer_create_params (:obj:`str`):
    """

    sessionid: str
    serverid: int
    partner: str
    tradeoffermessage: str
    json_tradeoffer: str
    captcha: str
    trade_offer_create_params: str

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['P2PTradeOffer']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.P2PTradeOffer`, optional: Данные для совершения p2p трейда.
        """

        if not cls.is_valid_model_data(data):
            return

        data = super(P2PTradeOffer, cls).de_json(data)

        return cls(**data)

@dataclass
class P2PSendObject(TraderClientObject):
    """Класс, представляющий ссылку на p2p трейд и сам трейд.

    Attributes:
        trade_link (:obj:`str`): Ссылка для p2p обмена.
        trade_offer (:class:`steam_trader.P2PTradeOffer`, optional): Параметры для POST запроса
            (https://steamcommunity.com/tradeoffer/new/send) при создании обмена в Steam. Вместо {sessionid} нужно
            указывать ID своей сессии в Steam.
    """

    trade_link: str
    trade_offer: Optional['P2PTradeOffer']

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['P2PSendObject']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.P2PSendObject`, optional: Ссылка на p2p трейд и сам трейд.
        """

        if not cls.is_valid_model_data(data):
            return

        data.update({  # перенос с camleCase на snake_case
            'trade_link': data['tradeLink'],
            'trade_offer': data['tradeOffer']
        })

        del data['tradeLink'], data['tradeOffer']

        data['trade_offer'] = P2PTradeOffer.de_json(data['trade_offer'])

        data = super(P2PSendObject, cls).de_json(data)

        return cls(**data)

@dataclass
class P2PReceiveObject(TraderClientObject):
    """Класс, представляющий массив с данными для принятия обмена.

    Attributes:
        offerid (:obj:`int`): ID обмена в Steam.
        code (:obj:`str`): Код проверки обмена.
        items (Sequence[`steam_trader.ExchangeItem`, optional]): Список предметов в обмене.
        partner_steamid (:obj:`int`): SteamID покупателя.
    """

    offerid: int
    code: str
    items: Sequence[Optional['ExchangeItem']]
    partner_steamid: int

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['P2PReceiveObject']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.P2PSendObject`, optional: Массив с данными для принятия обмена.
        """

        if not cls.is_valid_model_data(data):
            return

        data.update({  # перенос с camleCase на snake_case
            'offerid': data['offerId'],
            'partner_steamid': data['partnerSteamId']
        })

        del data['offerId'], data['partnerSteamId']

        for i, item in enumerate(data['items']):
            data['items'][i] = ExchangeItem.de_json(item)

        data = super(P2PReceiveObject, cls).de_json(data)

        return cls(**data)

@dataclass
class P2PConfirmObject(TraderClientObject):
    """Класс, представляющий массив с данными для подтверждения обмена в мобильном аутентификаторе.

    Attributes:
        offerid (:obj:`int`): ID обмена в Steam
        code (:obj:`str`): Код проверки обмена
        partner_steamid (:obj:`int`) SteamID покупателя
    """

    offerid: int
    code: str
    partner_steamid: int

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional['P2PConfirmObject']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:class:`steam_trader.Client`, optional): Клиент Steam Trader.

        Returns:
            :class:`steam_trader.P2PSendObject`, optional: Массив с данными для подтверждения обмена в мобильном аутентификаторе.
        """

        if not cls.is_valid_model_data(data):
            return

        data.update({  # перенос с camleCase на snake_case
            'offerid': data['offerId'],
            'partner_steamid': data['partnerSteamId']
        })

        del data['offerId'], data['partnerSteamId']

        data = super(P2PConfirmObject, cls).de_json(data)

        return cls(**data)
