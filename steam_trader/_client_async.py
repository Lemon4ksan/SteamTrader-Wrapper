import httpx
import logging
import functools
from typing import Optional, LiteralString, Union, Sequence, TypeVar, Callable, Any

from .constants import SUPPORTED_APPIDS
from .exceptions import BadRequestError, WrongTradeLink, SaveFail, UnsupportedAppID, Unauthorized
from ._base import TraderClientObject
from ._account import WSToken, Inventory, BuyOrders, Discounts, OperationsHistory, InventoryState, AltWebSocket
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


class ClientAsync(TraderClientObject):
    """Класс, представляющий клиент Steam Trader.

    Args:
        api_token (:obj:`str`): Уникальный ключ для аутентификации.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
        headers (:obj:`dict`, optional): Словарь, содержащий сведения об устройстве, с которого выполняются запросы.
            Используется при каждом запросе на сайт.

    Attributes:
        api_token (:obj:`str`): Уникальный ключ для аутентификации.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
        headers (:obj:`dict`, optional): Словарь, содержащий сведения об устройстве, с которого выполняются запросы.
            Используется при каждом запросе на сайт.
    """

    def __init__(
            self,
            api_token: str,
            *,
            base_url: Optional[str] = None,
            headers: Optional[dict] = None) -> None:

        self.api_token = api_token

        if base_url is None:
            base_url = "https://api.steam-trader.com/"
        self.base_url = base_url

        if headers is None:
            headers = {'user-agent': 'python3', 'wrapper': 'SteamTrader-Wrapper', 'manufacturer': 'Lemon4ksan'}
        self.headers = headers

    async def __aenter__(self):
        self._async_client = httpx.AsyncClient()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_client.aclose()

    @property
    async def balance(self) -> float:
        """Баланс клиента."""

        url = self.base_url + 'getbalance/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        result = result.json()
        if not result['success']:
            raise Unauthorized('Неправильный api-токен')
        return result['balance']

    @log
    async def sell(self, itemid: int, assetid: int, price: float) -> Optional['SellResult']:
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
            :class:`steam_trader.SellResult, optional`: Результат создания предложения о продаже.
        """

        url = self.base_url + 'sale/'
        result = await self._async_client.post(
            url,
            data={"itemid": itemid, "assetid": assetid, "price": price, "key": self.api_token},
            headers=self.headers
        )
        return SellResult.de_json(result.json(), self)

    @log
    async def buy(self, _id: Union[int, str], _type: int, price: float, currency: int = 1) -> Optional['BuyResult']:
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
            :class:`steam_trader.BuyResult`, optional: Результат создания запроса о покупке.
        """

        url = self.base_url + 'buy/'
        result = await self._async_client.post(
            url,
            data={"id": _id, "type": _type, "price": price, "currency": currency, "key": self.api_token},
            headers=self.headers
        )
        return BuyResult.de_json(result.json(), self)

    @log
    async def create_buy_order(self, gid: int, price: float, *, count: int = 1) -> Optional['BuyOrderResult']:
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
            :class:`steam_trader.BuyOrderResult, optional`: Результат созданния заявки на покупку.
        """

        url = self.base_url + 'createbuyorder/'
        result = await self._async_client.post(
            url,
            data={"gid": gid, "price": price, "count": count, "key": self.api_token},
            headers=self.headers
        )
        return BuyOrderResult.de_json(result.json(), self)

    @log
    async def multi_buy(self, gid: int, max_price: float, count: int) -> Optional['MultiBuyResult']:
        """Создать запрос о покупке нескольких предметов с определённым GID.

        Будут куплены самые лучшие (дешёвые) предложения о продаже.

        Если максимальная цена ПОКУПКИ будет указана больше, чем у имеющихся предложений о ПРОДАЖЕ, ПОКУПКА
        совершится по цене предложений. Например, на сайте есть 2 предложения о продаже по цене 10 и 11 ₽,
        если при покупке указать максмальную цену 25 ₽, то сделки совершатся по цене 10 и 11 ₽,
        а общая сумма потраченных средств - 21 ₽.

        Будет куплено указанное количество предметов. Если по указанной максимальной цене не окажется достаточно
        предложений о продаже, покупка завершится ошибкой.

        Args:
            gid (:obj:`int`): ID группы предметов.
            max_price (:obj:`float`): Максимальная цена одного предмета без учета комиссии/скидки.
            count (:obj:`int`): Количество предметов для покупки.

        Returns:
            :class:`steam_trader.MultiBuyResult`, optional: Результат создания запроса на мульти-покупку.
        """

        url = self.base_url + 'multibuy/'
        result = await self._async_client.post(
            url,
            data={"gid": gid, "max_price": max_price, "count": count, "key": self.api_token},
            headers=self.headers
        )
        return MultiBuyResult.de_json(result.json(), self)

    @log
    async def edit_price(self, _id: int, price: float) -> Optional['EditPriceResult']:
        """Редактировать цену предмета/заявки на покупку.

        При редактировании может произойти моментальная продажа/покупка по аналогии тому,
        как это сделано в методах sale и create_buy_order.

        Args:
            _id (:obj:`int`): ID предложения о продаже/заявки на покупку.
            price (:obj:`float`): Новая цена, за которую хотите продать/купить предмет без учёта комиссии/скидки.

        Returns:
            :class:`steam_trader.EditPriceResult`, optional: Результат запроса на изменение цены.
        """

        url = self.base_url + 'editprice/'
        result = await self._async_client.post(
            url,
            data={"id": _id, "price": price, "key": self.api_token},
            headers=self.headers
        )
        return EditPriceResult.de_json(result.json(), self)

    @log
    async def delete_item(self, _id: int) -> Optional['DeleteItemResult']:
        """Снять предмет с продажи/заявку на покупку.

        Args:
            _id (:obj:`int`): ID продажи/заявки на покупку.

        Returns:
            :class:`steam_trader.DeleteItemResult`, optional: Результат запроса снятия предмета
                с продажи/заявки на покупку.
        """

        url = self.base_url + 'deleteitem/'
        result = await self._async_client.post(
            url,
            data={"id": _id, "key": self.api_token},
            headers=self.headers
        )
        return DeleteItemResult.de_json(result.json(), self)

    @log
    async def get_down_orders(self, gameid: int, *, order_type: LiteralString = 'sell') -> Optional['GetDownOrdersResult']:
        """Снять все заявки на продажу/покупку предметов.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            order_type (:obj:`LiteralString`): Тип заявок для удаления:
                "sell" - предложения о ПРОДАЖЕ. Значение по умолчанию.
                "buy" - предложения о ПОКУПКЕ.

        Returns:
            :class:`steam_trader.GetDownOrdersResult`, optional: Результат снятия всех заявок
                на продажу/покупку предметов.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается')

        url = self.base_url + 'getdownorders/'
        result = await self._async_client.post(
            url,
            data={"gameid": gameid, "type": order_type, "key": self.api_token},
            headers=self.headers
        )
        return GetDownOrdersResult.de_json(result.json(), self)

    @log
    async def get_items_for_exchange(self) -> Optional['ItemsForExchange']:
        """Получить список предметов для обмена с ботом.

        Returns:
            :class:`steam_trader.ItemsForExchange`, optional: Cписок предметов для обмена с ботом.
        """

        url = self.base_url + 'itemsforexchange/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return ItemsForExchange.de_json(result.json(), self)

    @log
    async def exchange(self) -> Optional['ExchangeResult']:
        """Выполнить обмен с ботом.

        Note:
            Вы сами должны принять трейд в приложении Steam, у вас будет 3 часа на это.
            В противном случае трейд будет отменён.

        Returns:
            :class:`steam_trader.ExchangeResult`, optional: Результат обмена с ботом.
        """

        url = self.base_url + 'exchange/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return ExchangeResult.de_json(result.json(), self)

    @log
    async def get_items_for_exchange_p2p(self) -> Optional['ItemsForExchange']:
        """Получить список предметов для p2p обмена.

        Returns:
            :class:`steam_trader.ItemsForExchange`, optional: Cписок предметов для p2p обмена.
        """

        url = self.base_url + 'itemsforexchangep2p/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return ItemsForExchange.de_json(result.json(), self)

    @log
    async def exchange_p2p(self) -> Optional['ExchangeP2PResult']:
        """Выполнить p2p обмен.

        Note:
            Вы сами должны передать предмет боту из полученной информации, у вас будет 40 минут на это.
            В противном случае, трейд будет отменён.

        Returns:
            :class:`steam_trader.ExchangeP2PResult`, optional: Результат p2p обмена .
        """

        url = self.base_url + 'exchange/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return ExchangeP2PResult.de_json(result.json(), self)

    @log
    async def get_min_prices(self, gid: int, currency: int = 1) -> Optional['MinPrices']:
        """Получить минимальные/максимальные цены предмета.

        Note:
            Сайт пока работает только с рублями. Не меняйте значение currency.

        Args:
            gid (:obj:`int`): ID группы предметов.
            currency (:obj:`int`): Валюта, значение 1 - рубль.

        Returns:
            :class:`steam_trader.MinPrices`, optional: Минимальные/максимальные цены предмета.
        """

        url = self.base_url + "getminprices/"
        result = await self._async_client.get(
            url,
            params={"gid": gid, "currency": currency, "key": self.api_token},
            headers=self.headers
        )
        return MinPrices.de_json(result.json(), self)

    @log
    async def get_item_info(self, gid: int) -> Optional['ItemInfo']:
        """Получить информацию о группе предметов.

        Args:
            gid (:obj:`int`): ID группы предметов.

        Returns:
            :class:`steam_trader.ItemInfo`, optional: Информация о группе предметов.
        """

        url = self.base_url + "iteminfo/"
        result = await self._async_client.get(
            url,
            params={"gid": gid, "key": self.api_token},
            headers=self.headers
        )
        return ItemInfo.de_json(result.json(), self)

    @log
    async def get_order_book(
            self,
            gid: int,
            *,
            mode: LiteralString = 'all',
            limit: Optional[int] = None
    ) -> Optional['OrderBook']:
        """Получить заявки о покупке/продаже предмета.

        Args:
            gid (:obj:`int`): ID группы предметов.
            mode (:obj:`LiteralString`): Режим отображения
                "all" - отображать покупки и продажи. Значение по умолчанию.
                "sell" - отображать только заявки на ПРОДАЖУ.
                "buy" - отображать только заявки на ПОКУПКУ.
            limit (:obj:`int`, optional): Максимальное количество строк в списке. По умолчанию - неограниченно

        Returns:
            :class:`steam_trader.OrderBook`, optional: Заявки о покупке/продаже предмета.
        """

        url = self.base_url + "orderbook/"
        result = await self._async_client.get(
            url,
            params={"gid": gid, "mode": mode, "limit": limit, "key": self.api_token},
            headers=self.headers
        )
        return OrderBook.de_json(result.json(), self)

    @log
    async def get_web_socket_token(self) -> Optional['WSToken']:
        """Возварщает токен для авторизации в WebSocket. Незадокументированно."""
        url = self.base_url + "getwstoken/"
        result = await self._async_client.get(url)
        return WSToken.de_json(result.json(), self)

    @log
    async def get_inventory(self, gameid: int, *, status: Optional[Sequence[int]] = None) -> Optional['Inventory']:
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        По умолчанию (то есть всегда) возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Note:
            Аргумент status не работает.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            status (Sequence[:obj:`int`], optional): Указывается, чтобы получить список предметов с определенным статусом.

                Возможные статусы:
                0 - В продаже
                1 - Принять
                2 - Передать
                3 - Ожидается
                4 - Заявка на покупку

                Если не указавать, вернётся список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Returns:
            :class:`steam_trader.Inventory`, optional: Инвентарь клиента, включая заявки на покупку и купленные предметы.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается')

        url = self.base_url + 'getinventory/'
        result = await self._async_client.get(
            url,
            params={"gameid": gameid, 'status': status, "key": self.api_token},
            headers=self.headers
        )
        return Inventory.de_json(result.json(), self)

    @log
    async def get_buy_orders(self, *, gameid: Optional[int] = None, gid: Optional[int] = None) -> Optional['BuyOrders']:
        """Получить последовательность заявок на покупку. По умолчанию возвращаются заявки для всех
        предметов из всех разделов.

        При указании соответствующих параметров можно получить заявки из определённого раздела и/или предмета.

        Note:
            Во время тестирования мои запросы на покупку отображались только тогда,
            когда я указал конкретный appid игры и gid предмета.

        Args:
            gameid (:obj:`int`, optional): AppID приложения в Steam.
            gid (:obj:`int`, optional): ID группы предметов.

        Returns:
            :class:`steam_trader.BuyOrders`, optional: Список заявок на покупку.
        """

        if gameid is not None and gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается')

        url = self.base_url + 'getbuyorders/'
        result = await self._async_client.get(
            url,
            params={"gameid": gameid, 'gid': gid, "key": self.api_token},
            headers=self.headers
        )
        return BuyOrders.de_json(result.json(), self)

    @log
    async def get_discounts(self) -> Optional['Discounts']:
        """Получить комиссии/скидки и оборот на сайте.

        Данные хранятся в словаре data, где ключ - это AppID игры в Steam (См. steam_trader.constants).

        Returns:
            :class:`steam_trader.Discounts`, optional: Комиссии/скидки и оборот на сайте.
        """

        url = self.base_url + 'getdiscounts/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return Discounts.de_json(result.json(), self)

    @log
    async def set_trade_link(self, trade_link: str) -> None:
        """Установить ссылку для обмена.

        Args:
            trade_link (:obj:`str`): Ссылка для обмена,
                Например, https://steamcommunity.com/tradeoffer/new/?partner=453486961&token=ZhXMbDS9
        """

        url = self.base_url + 'settradelink/'
        result = await self._async_client.post(
            url,
            data={"trade_link": trade_link, "key": self.api_token},
            headers=self.headers
        )
        result = result.json()

        if not result['success']:
            try:
                match result['code']:
                    case 400:
                        raise BadRequestError('Неправильный запрос')
                    case 401:
                        raise Unauthorized('Неправильный api-токен')
                    case 1:
                        raise SaveFail('Не удалось сохранить ссылку обмена')
            except KeyError:
                raise WrongTradeLink('Вы указали ссылку для обмена от другого Steam аккаунта')

    @log
    async def remove_trade_link(self) -> None:
        """Удалить ссылку для обмена."""

        url = self.base_url + 'removetradelink/'
        result = await self._async_client.post(
            url,
            data={"trade_link": "1", "key": self.api_token},
            headers=self.headers
        )
        result = result.json()

        if not result['success']:
            match result['code']:
                case 400:
                    raise BadRequestError('Неправильный запрос')
                case 401:
                    raise Unauthorized('Неправильный api-токен')
                case 1:
                    raise SaveFail('Не удалось удалить ссылку обмена')

    @log
    async def get_operations_history(self, *, operation_type: Optional[int] = None) -> Optional['OperationsHistory']:
        """Получить историю операций (По умолчанию все типы).

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

        Returns:
              :class:`steam_trader.OperationsHistory`, optional: История операций.
        """

        url = self.base_url + 'operationshistory/'
        result = await self._async_client.get(
            url,
            params={"type": operation_type, "key": self.api_token},
            headers=self.headers
        )
        return OperationsHistory.de_json(result.json(), self)

    @log
    async def update_inventory(self, gameid: int) -> None:
        """Обновить инвентарь игры на сайте.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается')

        url = self.base_url + 'updateinventory/'
        result = await self._async_client.get(
            url,
            params={"gameid": gameid, "key": self.api_token},
            headers=self.headers
        )
        result = result.json()

        if not result['success']:
            match result['code']:
                case 401:
                    raise Unauthorized('Неправильный api-токен')

    @log
    async def get_inventory_state(self, gameid: int) -> Optional['InventoryState']:
        """Получить текущий статус обновления инвентаря.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.

        Returns:
            :class:`steam_trader.InventoryState`, optional: Текущий статус обновления инвентаря.
        """

        if gameid not in SUPPORTED_APPIDS:
            raise UnsupportedAppID(f'Игра с AppID {gameid}, в данный момент не поддерживается')

        url = self.base_url + 'inventorystate/'
        result = await self._async_client.get(
            url,
            params={"gameid": gameid, "key": self.api_token},
            headers=self.headers
        )
        return InventoryState.de_json(result.json(), self)

    @log
    async def trigger_alt_web_socket(self) -> Optional['AltWebSocket']:
        """Создать запрос альтернативным WebSocket.
        Для поддержания активного соединения нужно делать этот запрос каждые 2 минуты.

        Returns:
            :class:`steam_trader.AltWebSocket`, optional: Запрос альтернативным WebSocket.
        """

        url = self.base_url + 'altws/'
        result = await self._async_client.get(
            url,
            params={"key": self.api_token},
            headers=self.headers
        )
        return AltWebSocket.de_json(result.json(), self)
