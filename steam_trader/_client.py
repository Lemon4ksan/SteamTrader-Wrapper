import httpx
import logging
import functools
from collections.abc import Sequence, Callable
from typing import Optional, LiteralString, Union, TypeVar, Any

from .constants import SUPPORTED_APPIDS
from .exceptions import BadRequestError, WrongTradeLink, SaveFail, UnsupportedAppID, Unauthorized, TooManyRequests
from ._base import TraderClientObject
from ._account import WebSocketToken, Inventory, BuyOrders, Discounts, OperationsHistory, InventoryState, AltWebSocket
from ._buy import BuyResult, BuyOrderResult, MultiBuyResult
from ._sale import SellResult
from ._edit_item import EditPriceResult, DeleteItemResult, GetDownOrdersResult
from ._item_info import MinPrices, ItemInfo, OrderBook
from ._trade import ItemsForExchange, ExchangeResult, ExchangeP2PResult


logging.getLogger(__name__).addHandler(logging.NullHandler())

F = TypeVar('F', bound=Callable[..., Any])

def log(method: F) -> F:
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(f'Entering: {method.__name__}')

        result = method(*args, **kwargs)
        logger.info(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper


class Client(TraderClientObject):
    """Класс, представляющий клиент Steam Trader.

    Args:
        api_token (:obj:`str`): Уникальный ключ для аутентификации.
        proxy (:obj:`str`, optional): Прокси для запросов. Для работы необходимо использовать контекстный менеджер with.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
        headers (:obj:`dict`, optional): Словарь, содержащий сведения об устройстве, с которого выполняются запросы.
            Используется при каждом запросе на сайт.

    Attributes:
        api_token (:obj:`str`): Уникальный ключ для аутентификации.
        proxy (:obj:`str`, optional): Прокси для запросов.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
        headers (:obj:`dict`, optional): Словарь, содержащий сведения об устройстве, с которого выполняются запросы.
            Используется при каждом запросе на сайт.

    Raises:
        BadRequestError: Неправильный запрос.
        Unauthorized: Неправильный api-токен.
        TooManyRequests: Слишком много запросов.
    """

    def __init__(
            self,
            api_token: str,
            *,
            proxy: Optional[str] = None,
            base_url: Optional[str] = None,
            headers: Optional[dict] = None) -> None:

        self.api_token = api_token

        if base_url is None:
            base_url = "https://api.steam-trader.com/"
        self.base_url = base_url

        if headers is None:
            headers = {
                'user-agent': 'python3',
                'wrapper': 'SteamTrader-Wrapper',
                'manufacturer': 'Lemon4ksan',
                "Api-Key": self.api_token
            }
        self.headers = headers

        self._httpx_client = None
        self.proxy = proxy

    def __enter__(self) -> 'Client':
        self._httpx_client = httpx.Client(proxy=self.proxy)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._httpx_client.close()

    @property
    def balance(self) -> float:
        """Баланс клиента."""

        url = self.base_url + 'getbalance/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()
        if not result['success']:
            match result['code']:
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')
        return result['balance']

    @log
    def sell(self, itemid: int, assetid: int, price: float) -> 'SellResult':
        """Создать предложение о продаже определённого предмета.

        Note:
            Если при создании предложения о ПРОДАЖЕ указать цену меньше, чем у имеющейся заявки на ПОКУПКУ,
            предложение о ПРОДАЖЕ будет исполнено моментально по цене заявки на ПОКУПКУ.
            Например, на сайте есть заявка на покупку за 10 ₽, а продавец собирается выставить предложение за 5 ₽
            (дешевле), то сделка совершится по цене 10 ₽.

        Args:
            itemid (:obj:`int`): Уникальный ID предмета.
            assetid (:obj:`int`): AssetID предмета в Steam (найти их можно через get_inventory).
            price (:obj:`float`): Цена, за которую хотите продать предмет без учёта комиссии/скидки.

        Returns:
            :class:`steam_trader.SellResult`: Результат создания предложения о продаже.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
            NoTradeLink: Отсутствует сслыка для обмена.
            IncorrectPrice: Неправильная цена заявки.
            ItemAlreadySold: Предмет уже продан или отстутствует.
            AuthenticatorError: Мобильный аутентификатор не подключён
                или с момента его подключения ещё не прошло 7 дней.
        """

        url = self.base_url + 'sale/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"itemid": itemid, "assetid": assetid, "price": price},
            headers=self.headers
        ).json()
        return SellResult.de_json(result, self)

    @log
    def buy(self, _id: Union[int, str], _type: int, price: float, currency: int = 1) -> 'BuyResult':
        """Создать предложение о покупке предмета по строго указанной цене.

        Если в момент покупки цена предложения о продаже изменится, покупка не совершится.

        Note:
            Сайт пока работает только с рублями. Не меняйте значение currency.

        Args:
            _id (:obj:`int | :obj: str`): В качества ID может выступать:
                GID для варианта покупки Commodity.
                Часть ссылки после nc/ (nc/L8RJI7XR96Mmo3Bu) для варианта покупки NoCommission.
                ID предложения о продаже для варианта покупки Offer (найти их можно в ItemInfo).
            _type (:obj:`int`): Вариант покупки (указаны выше) - 1 / 2 / 3.
            price (:obj:`float`): Цена предложения о продаже без учёта комиссии/скидки.
                Актуальные цены можно узнать через get_item_info и get_min_prices.
            currency (:obj:`int`): Валюта покупки. Значение 1 - рубль.

        Returns:
            :class:`steam_trader.BuyResult`: Результат создания запроса о покупке.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            NoTradeLink: Отсутствует сслыка для обмена.
            NoLongerExists: Предложение больше недействительно.
            NotEnoughMoney: Недостаточно средств.
        """

        url = self.base_url + 'buy/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"id": _id, "type": _type, "price": price, "currency": currency},
            headers=self.headers
        ).json()
        return BuyResult.de_json(result, self)

    @log
    def create_buy_order(self, gid: int, price: float, *, count: int = 1) -> 'BuyOrderResult':
        """Создать заявку на покупку предмета с определённым GID.

        Note:
            Если при создании предложения о ПРОДАЖЕ указать цену меньше, чем у имеющейся заявки на ПОКУПКУ,
            предложение о ПРОДАЖЕ будет исполнено моментально по цене заявки на ПОКУПКУ.
            Например, на сайте есть заявка на покупку за 10 ₽, а продавец собирается выставить предложение за 5 ₽
            (дешевле), то сделка совершится по цене 10 ₽.

        Args:
            gid (:obj:`int`): ID группы предметов.
            price (:obj:`float`): Цена предмета, за которую будете его покупать без учёта комиссии/скидки.
            count (:obj:`int`): Количество заявок для размещения (не более 500). По умолчанию - 1.

        Returns:
            :class:`steam_trader.BuyOrderResult`: Результат созданния заявки на покупку.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
            NoTradeLink: Отсутствует сслыка для обмена.
            NoLongerExists: Предложение больше недействительно.
            NotEnoughMoney: Недостаточно средств.
            AssertionError: Указаны недопустимые параметры.
        """

        assert 1 <= count <= 500, f'Количество заявок должно быть от 1 до 500 (не {count})'

        url = self.base_url + 'createbuyorder/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"gid": gid, "price": price, "count": count},
            headers=self.headers
        ).json()
        return BuyOrderResult.de_json(result, self)

    @log
    def multi_buy(self, gid: int, max_price: float, count: int) -> 'MultiBuyResult':
        """Создать запрос о покупке нескольких предметов с определённым GID.

        Будут куплены самые лучшие (дешёвые) предложения о продаже.

        Если максимальная цена ПОКУПКИ будет указана больше, чем у имеющихся предложений о ПРОДАЖЕ, ПОКУПКА
        совершится по цене предложений. Например, на сайте есть 2 предложения о продаже по цене 10 и 11 ₽,
        если при покупке указать максмальную цену 25 ₽, то сделки совершатся по цене 10 и 11 ₽,
        а общая сумма потраченных средств - 21 ₽.

        Если по указанной максимальной цене не окажется достаточно предложений о продаже,
        success будет равен False и будет указано кол-во оставшихся предметов по данной цене.

        Args:
            gid (:obj:`int`): ID группы предметов.
            max_price (:obj:`float`): Максимальная цена одного предмета без учета комиссии/скидки.
            count (:obj:`int`): Количество предметов для покупки.

        Returns:
            :class:`steam_trader.MultiBuyResult`: Результат создания запроса на мульти-покупку.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            NoTradeLink: Отсутствует сслыка для обмена.
            NotEnoughMoney: Недостаточно средств.

        Changes:
            0.2.3: Теперь, если во время операции закончиться баланс, вместо ошибки,
                в датаклассе будет указано кол-во оставшихся предметов по данной цене.
        """

        url = self.base_url + 'multibuy/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"gid": gid, "max_price": max_price, "count": count},
            headers=self.headers
        ).json()
        return MultiBuyResult.de_json(result, self)

    @log
    def edit_price(self, _id: int, price: float) -> 'EditPriceResult':
        """Редактировать цену предмета/заявки на покупку.

        При редактировании может произойти моментальная продажа/покупка по аналогии тому,
        как это сделано в методах sell и create_buy_order.

        Args:
            _id (:obj:`int`): ID предложения о продаже/заявки на покупку.
            price (:obj:`float`): Новая цена, за которую хотите продать/купить предмет без учёта комиссии/скидки.

        Returns:
            :class:`steam_trader.EditPriceResult`: Результат запроса на изменение цены.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            UnknownItem: Предмет не был найден.
            IncorrectPrice: Неправильная цена заявки.
            NotEnoughMoney: Недостаточно средств.
        """

        url = self.base_url + 'editprice/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"id": _id, "price": price},
            headers=self.headers
        ).json()
        return EditPriceResult.de_json(result, self)

    @log
    def delete_item(self, _id: int) -> 'DeleteItemResult':
        """Снять предмет с продажи/заявку на покупку.

        Args:
            _id (:obj:`int`): ID продажи/заявки на покупку.

        Returns:
            :class:`steam_trader.DeleteItemResult`: Результат запроса снятия предмета
                с продажи/заявки на покупку.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
        """

        url = self.base_url + 'deleteitem/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"id": _id},
            headers=self.headers
        ).json()
        return DeleteItemResult.de_json(result, self)

    @log
    def get_down_orders(self, gameid: int, *, order_type: LiteralString = 'sell') -> 'GetDownOrdersResult':
        """Снять все заявки на продажу/покупку предметов.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            order_type (:obj:`LiteralString`): Тип заявок для удаления:
                "sell" - предложения о ПРОДАЖЕ. Значение по умолчанию.
                "buy" - предложения о ПОКУПКЕ.

        Returns:
            :class:`steam_trader.GetDownOrdersResult`: Результат снятия всех заявок
                на продажу/покупку предметов.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            NoTradeItems: Нет заявок на продажу/покупку.
            UnsupportedAppID: Указан недействительный gameid.
            ValueError: Указано недопустимое значение order_type.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается.')

        if order_type not in ['sell', 'buy']:
            raise ValueError(f'Неизвестный тип {order_type}')

        url = self.base_url + 'getdownorders/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"gameid": gameid, "type": order_type},
            headers=self.headers
        ).json()
        return GetDownOrdersResult.de_json(result, self)

    @log
    def get_items_for_exchange(self) -> 'ItemsForExchange':
        """Получить список предметов для обмена с ботом.

        Returns:
            :class:`steam_trader.ItemsForExchange`: Cписок предметов для обмена с ботом.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            NoTradeItems: Нет предметов для обмена.
        """

        url = self.base_url + 'itemsforexchange/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()
        return ItemsForExchange.de_json(result, self)

    @log
    def exchange(self) -> 'ExchangeResult':
        """Выполнить обмен с ботом.

        Note:
            Вы сами должны принять трейд в приложении Steam, у вас будет 3 часа на это.
            В противном случае трейд будет отменён.

        Returns:
            :class:`steam_trader.ExchangeResult`: Результат обмена с ботом.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            NoTradeLink: Отсутствует сслыка для обмена.
            TradeCreationFail: Не удалось создать предложение обмена или бот не может отправить предложение обмена,
                так как обмены в Steam временно не работают, или ваш инвентарь переполнен, или у вас есть VAC бан.
            NoTradeItems: Нет предметов для обмена.
            ExpiredTradeLink: Ссылка для обмена больше недействительна.
            TradeBlockError: Steam Guard не подключён или стоит блокировка обменов.
            MissingRequiredItems: В инвентаре Steam отсутствуют необходимые для передачи предметы.
            HiddenInventory: Ваш инвентарь скрыт.
            AuthenticatorError: Мобильный аутентификатор не подключён,
                или с момента его подключения ещё не прошло 7 дней.
        """

        url = self.base_url + 'exchange/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()
        return ExchangeResult.de_json(result, self)

    @log
    def get_items_for_exchange_p2p(self) -> 'ItemsForExchange':
        """Получить список предметов для p2p обмена.

        Returns:
            :class:`steam_trader.ItemsForExchange`: Cписок предметов для p2p обмена.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            NoTradeItems: Нет предметов для обмена.
        """

        url = self.base_url + 'itemsforexchangep2p/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()

        return ItemsForExchange.de_json(result, self)

    @log
    def exchange_p2p(self) -> 'ExchangeP2PResult':
        """Выполнить p2p обмен.

        Note:
            Вы сами должны передать предмет клиенту из полученной информации, у вас будет 40 минут на это.
            В противном случае, трейд будет отменён.

        Returns:
            :class:`steam_trader.ExchangeP2PResult`: Результат p2p обмена.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            NoTradeLink: Отсутствует сслыка для обмена.
            TradeCreationFail: Не удалось создать предложение обмена или бот не может отправить предложение обмена,
                так как обмены в Steam временно не работают, или ваш инвентарь переполнен, или у вас есть VAC бан,
                или покупатель не указал свою ссылку для обмена.
            NoTradeItems: Нет предметов для обмена.
            NoSteamAPIKey: Отсутсвтвует ключ Steam API.
            AuthenticatorError: Мобильный аутентификатор не подключён,
                или с момента его подключения ещё не прошло 7 дней.
        """

        url = self.base_url + 'exchange/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()

        return ExchangeP2PResult.de_json(result, self)

    @log
    def get_min_prices(self, gid: int, currency: int = 1) -> 'MinPrices':
        """Получить минимальные/максимальные цены предмета.

        Note:
            Сайт пока работает только с рублями. Не меняйте значение currency.

        Args:
            gid (:obj:`int`): ID группы предметов.
            currency (:obj:`int`): Валюта, значение 1 - рубль.

        Returns:
            :class:`steam_trader.MinPrices`: Минимальные/максимальные цены предмета.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
        """

        url = self.base_url + "getminprices/"
        result = (self._httpx_client or httpx).get(
            url,
            params={"gid": gid, "currency": currency},
            headers=self.headers
        ).json()
        return MinPrices.de_json(result, self)

    @log
    def get_item_info(self, gid: int) -> 'ItemInfo':
        """Получить информацию о группе предметов.

        Args:
            gid (:obj:`int`): ID группы предметов.

        Returns:
            :class:`steam_trader.ItemInfo`: Информация о группе предметов.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
        """

        url = self.base_url + "iteminfo/"
        result = (self._httpx_client or httpx).get(
            url,
            params={"gid": gid},
            headers=self.headers
        ).json()
        return ItemInfo.de_json(result, self)

    @log
    def get_order_book(self, gid: int, *, mode: LiteralString = 'all', limit: Optional[int] = None) -> 'OrderBook':
        """Получить заявки о покупке/продаже предмета.

        Args:
            gid (:obj:`int`): ID группы предметов.
            mode (:obj:`LiteralString`): Режим отображения
                "all" - отображать покупки и продажи. Значение по умолчанию.
                "sell" - отображать только заявки на ПРОДАЖУ.
                "buy" - отображать только заявки на ПОКУПКУ.
            limit (:obj:`int`, optional): Максимальное количество строк в списке. По умолчанию - неограниченно

        Returns:
            :class:`steam_trader.OrderBook`: Заявки о покупке/продаже предмета.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            ValueError: Указано недопустимое значение mode.
        """

        if mode not in ['all', 'sell', 'buy']:
            raise ValueError(f'Неизвестный режим {mode}')

        url = self.base_url + "orderbook/"
        result = (self._httpx_client or httpx).get(
            url,
            params={"gid": gid, "mode": mode, "limit": limit},
            headers=self.headers
        ).json()
        return OrderBook.de_json(result, self)

    @log
    def get_web_socket_token(self) -> 'WebSocketToken':
        """Получить токен для авторизации в WebSocket. Незадокументированно."""
        url = self.base_url + "getwstoken/"
        result = (self._httpx_client or httpx).get(
            url,
            params={'key': self.api_token}
        ).json()
        return WebSocketToken.de_json(result, self)

    @log
    def get_inventory(self, gameid: int, *, status: Optional[Sequence[int]] = None) -> 'Inventory':
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        По умолчанию возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            status (Sequence[:obj:`int`], optional):
                Указывается, чтобы получить список предметов с определенным статусом.

                Возможные статусы:
                0 - В продаже
                1 - Принять
                2 - Передать
                3 - Ожидается
                4 - Заявка на покупку

        Returns:
            :class:`steam_trader.Inventory`: Инвентарь клиента, включая заявки на покупку и купленные предметы.

        Raises:
            UnsupportedAppID: Указан недействительный gameid.
            ValueError: Указан недопустимый статус.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается.')

        url = self.base_url + 'getinventory/'
        params = {"gameid": gameid}

        if status is not None:
            for i, s in enumerate(status):
                if s not in range(5):
                    raise ValueError(f'Неизвестный статус {s}')
                params[f'status[{i}]'] = s

        result = (self._httpx_client or httpx).get(
            url,
            params=params,
            headers=self.headers
        ).json()
        return Inventory.de_json(result, status, self)

    @log
    def get_buy_orders(self, *, gameid: Optional[int] = None, gid: Optional[int] = None) -> 'BuyOrders':
        """Получить последовательность заявок на покупку. По умолчанию возвращаются заявки для всех
        предметов из всех разделов.

        При указании соответствующих параметров можно получить заявки из определённого раздела и/или предмета.

        Args:
            gameid (:obj:`int`, optional): AppID приложения в Steam.
            gid (:obj:`int`, optional): ID группы предметов.

        Returns:
            :class:`steam_trader.BuyOrders`: Список заявок на покупку.

        Raises:
            UnsupportedAppID: Указан недействительный gameid.
            NoBuyOrders: Нет запросов на покупку.
        """

        if gameid is not None and gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается.')

        params = {}
        if gameid is not None:
            params['gameid'] = gameid
        if gid is not None:
            params['gid'] = gid

        url = self.base_url + 'getbuyorders/'
        result = (self._httpx_client or httpx).get(
            url,
            params=params,
            headers=self.headers
        ).json()
        return BuyOrders.de_json(result, self)

    @log
    def get_discounts(self) -> 'Discounts':
        """Получить комиссии/скидки и оборот на сайте.

        Данные хранятся в словаре data, где ключ - это AppID игры в Steam (См. steam_trader.constants).

        Returns:
            :class:`steam_trader.Discounts`: Комиссии/скидки и оборот на сайте.
        """

        url = self.base_url + 'getdiscounts/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()
        return Discounts.de_json(result, self)

    @log
    def set_trade_link(self, trade_link: str) -> None:
        """Установить ссылку для обмена.

        Args:
            trade_link (:obj:`str`): Ссылка для обмена,
                Например, https://steamcommunity.com/tradeoffer/new/?partner=453486961&token=ZhXMbDS9

        Raises:
            SaveFail: Не удалось сохранить ссылку обмена.
            WrongTradeLink: Указана ссылка для обмена от другого Steam аккаунта ИЛИ ссылка для обмена уже указана.
        """

        url = self.base_url + 'settradelink/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"trade_link": trade_link},
            headers=self.headers
        ).json()

        if not result['success']:
            try:
                match result['code']:
                    case 400:
                        raise BadRequestError('Неправильный запрос.')
                    case 401:
                        raise Unauthorized('Неправильный api-токен.')
                    case 429:
                        raise TooManyRequests('Вы отправили слишком много запросов.')
                    case 1:
                        raise SaveFail('Не удалось сохранить ссылку обмена.')
            except KeyError:
                raise WrongTradeLink('Указана ссылка для обмена от другого Steam аккаунта ИЛИ ссылка для обмена уже указана.')

    @log
    def remove_trade_link(self) -> None:
        """Удалить ссылку для обмена.

        Raises:
            SaveFail: Не удалось удалить ссылку обмена.
        """

        url = self.base_url + 'removetradelink/'
        result = (self._httpx_client or httpx).post(
            url,
            data={"trade_link": "1"},
            headers=self.headers
        ).json()

        if not result['success']:
            match result['code']:
                case 401:
                    raise Unauthorized('Неправильный api-токен.')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')
                case 1:
                    raise SaveFail('Не удалось удалить ссылку обмена.')

    @log
    def get_operations_history(self, *, operation_type: Optional[int] = None, page: int = 0) -> 'OperationsHistory':
        """Получить историю операций (По умолчанию все типы). В каждой странице до 100 пунктов.

        Args:
            operation_type (:obj:`int`, optional): Тип операции. Может быть пустым.
                Принимает значения:
                1 - Покупка предмета
                2 - Продажа предмета
                3 - Возврат за покупку
                4 - Пополнение баланса
                5 - Вывести средства
                9 - Ожидание покупки
                10 - Штрафной балл
            page (:obj:`int`): Страница операций. Отсчёт начинается с 0.

        Returns:
              :class:`steam_trader.OperationsHistory`: История операций.

        Raises:
            ValueError: Указано недопустимое значение operation_type.

        Changes:
            0.3.0: Добавлен аргумент page.
        """

        if operation_type not in range(1, 11) and operation_type is not None:
            raise ValueError(f'Неизвестный тип {operation_type}')

        url = self.base_url + 'operationshistory/'
        result = (self._httpx_client or httpx).get(
            url,
            params={"type": operation_type, "page": page},
            headers=self.headers
        ).json()
        return OperationsHistory.de_json(result, self)

    @log
    def update_inventory(self, gameid: int) -> None:
        """Обновить инвентарь игры на сайте.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.

        Raises:
            UnsupportedAppID: Указан недействительный gameid.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается.')

        url = self.base_url + 'updateinventory/'
        result = (self._httpx_client or httpx).get(
            url,
            params={"gameid": gameid},
            headers=self.headers
        ).json()

        if not result['success']:
            match result['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос.')
                case 401:
                    raise Unauthorized('Неправильный api-токен')
                case 429:
                    raise TooManyRequests('Вы отправили слишком много запросов.')

    @log
    def get_inventory_state(self, gameid: int) -> 'InventoryState':
        """Получить текущий статус обновления инвентаря.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.

        Returns:
            :class:`steam_trader.InventoryState`: Текущий статус обновления инвентаря.

        Raises:
            UnsupportedAppID: Указан недействительный gameid.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается.')

        url = self.base_url + 'inventorystate/'
        result = (self._httpx_client or httpx).get(
            url,
            params={"gameid": gameid},
            headers=self.headers
        ).json()
        return InventoryState.de_json(result, self)

    @log
    def trigger_alt_web_socket(self) -> Optional['AltWebSocket']:
        """Создать запрос альтернативным WebSocket.
        Для поддержания активного соединения нужно делать этот запрос каждые 2 минуты.

        Возвращает None если новых сообщений нет. При этом соединение будет поддрежано.

        Returns:
            :class:`steam_trader.AltWebSocket`, optional: Запрос альтернативным WebSocket.
        """

        url = self.base_url + 'altws/'
        result = (self._httpx_client or httpx).get(
            url,
            headers=self.headers
        ).json()
        return AltWebSocket.de_json(result, self)
