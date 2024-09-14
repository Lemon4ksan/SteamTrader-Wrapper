from dataclasses import dataclass
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from steam_trader import exceptions
from ._base import TraderClientObject
from ._misc import TradeDescription, ItemForExchange, ExchangeItem
from ._p2p import P2PConfirmObject, P2PReceiveObject, P2PSendObject

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

@dataclass
class ItemsForExchange(TraderClientObject):
    """Класс, представляющий предметы для обмена с ботом.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        items (Sequence[`steam_trader.ItemForExchange`]): Последовательность предметов для обмена с ботом.
        descriptions (dict[:obj:`int`, :class:`steam_trader.TradeDescription`]): Описания предметов
            для обмена с ботом. Ключ - itemid предмета.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    items: Sequence['ItemForExchange']
    descriptions: dict[int, 'TradeDescription']
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'ItemsForExchange':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.ItemsForExchange`: Предметы для обмена с ботом.
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
                    raise exceptions.InternalError('При выполнении запроса произошла неизвестная ошибка.')
                case 2:
                    raise exceptions.NoTradeItems('Нет предметов для обмена.')

        for i, item in enumerate(data['items']):
            data['items'][i] = ItemForExchange.de_json(item)

        # Конвертируем ключ в число
        data['descriptions'] = {
            int(_id): TradeDescription.de_json(_dict) for _id, _dict in data['descriptions'].items()
        }
        data = super(ItemsForExchange, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class ExchangeResult(TraderClientObject):
    """Класс, представляющий результат инициализации обмена с ботом.

    Attributes:
        success: (:obj:`bool`): Результат запроса.
        offer_id (:obj:`int`): ID обмена в Steam.
        code (:obj:`str`): Код проверки обмена.
        bot_steamid (:obj:`int`): SteamID бота, который отправил обмен.
        bot_nick (:obj:`str`): Ник бота.
        items (Sequence[:class:`steam_trader.ExchangeItem`]): Cписок предметов для обмена с ботом.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    offer_id: int
    code: str
    bot_steamid: int
    bot_nick: str
    items: Sequence['ExchangeItem']
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict,  client: Union['Client', 'ClientAsync', None] = None) -> 'ExchangeResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.ExchangeResult`: Результат обмена с ботом.
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
                    raise exceptions.InternalError('При выполнении запроса произошла неизвестная ошибка.')
                case 2:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 3:
                    raise exceptions.TradeCreationFail('Не удалось создать предложение обмена. Повторите попытку позже.')
                case 4:
                    raise exceptions.NoTradeItems('Нет предметов для обмена.')
                case 5:
                    raise exceptions.ExpiredTradeLink('Ссылка для обмена больше недействительна.')
                case 6:
                    raise exceptions.TradeBlockError('Steam Guard не подключён или стоит блокировка обменов.')
                case 7:
                    raise exceptions.TradeCreationFail('Бот не может отправить предложение обмена, так как обмены в Steam временно не работают.')
                case 8:
                    raise exceptions.MissingRequiredItems('В инвентаре Steam отсутствуют необходимые для передачи предметы.')
                case 9:
                    raise exceptions.HiddenInventory('Ваш инвентарь скрыт.')
                case 10:
                    raise exceptions.TradeCreationFail('Бот не может отправить вам предложение обмена, потому что ваш инвентарь переполнен или у вас есть VAC бан.')
                case 11:
                    raise exceptions.AuthenticatorError('Мобильный аутентификатор не подключён, или с момента его подключения ещё не прошло 7 дней.')

        data.update({  # перенос с camleCase на snake_case
            'offer_id': data['offerId'],
            'bot_steamid': data['botSteamId'],
            'bot_nick': data['botNick']
        })
        del data['offerId'], data['botSteamId'], data['botNick']

        for i, item in enumerate(data['items']):
            data['items'][i] = ExchangeItem.de_json(item)

        data = super(ExchangeResult, cls).de_json(data)

        return cls(client=client, **data)

@dataclass
class ExchangeP2PResult(TraderClientObject):
    """Класс, представляющий результат инициализации p2p обмена.

    Attributes:
        success (:obj:`bool`): Результат запроса.
        send (Sequence[:class:`steam_trader.P2PSendObject`]): Массив с данными для создания
            нового обмена в Steam.
        receive (Sequence[:class:`steam_trader.RecieveObject`]): Массив с данными для принятия обмена.
        confirm (Sequence[:class:`steam_trader.ConfirmObject`]): Массив с данными для подтверждения
            обмена в мобильном аутентификаторе.
        cancel (Sequence[:obj:`str`]): Массив из ID обменов, которые нужно отменить.
        client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
            Клиент Steam Trader.
    """

    success: bool
    send: Sequence['P2PSendObject']
    receive: Sequence['P2PReceiveObject']
    confirm: Sequence['P2PConfirmObject']
    cancel: Sequence[str]
    client: Union['Client', 'ClientAsync', None]

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> 'ExchangeP2PResult':
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]):
                Клиент Steam Trader.

        Returns:
            :class:`steam_trader.ExchangeP2PResult`: Результат p2p обмена.
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
                    raise exceptions.InternalError('При выполнении запроса произошла неизвестная ошибка.')
                case 2:
                    raise exceptions.NoTradeLink('Отсутствует сслыка для обмена.')
                case 3:
                    raise exceptions.TradeCreationFail('Не удалось создать предложение обмена. Повторите попытку позже.')
                case 4:
                    raise exceptions.NoTradeItems('Нет предметов для обмена.')
                case 5:
                    raise exceptions.NoSteamAPIKey('Отсутсвтвует ключ Steam API.')
                case 6:
                    raise exceptions.TradeCreationFail('Невозможно создать обмен. Покупатель не указал свою ссылку для обмена.')
                case 7:
                    raise exceptions.AuthenticatorError('Мобильный аутентификатор не подключён, или с момента его подключения ещё не прошло 7 дней.')

        for i, item in enumerate(data['send']):
            data['send'][i] = P2PSendObject.de_json(item)

        for i, item in enumerate(data['receive']):
            data['receive'][i] = P2PReceiveObject.de_json(item)

        for i, item in enumerate(data['confirm']):
            data['confirm'][i] = P2PConfirmObject.de_json(item)

        data = super(ExchangeP2PResult, cls).de_json(data)

        return cls(client=client, **data)
