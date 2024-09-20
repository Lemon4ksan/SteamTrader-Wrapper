import asyncio
import logging
import functools
from typing import Optional, Sequence, TypeVar, Callable, Any, LiteralString

from ._misc import TradeMode, PriceRange

from steam_trader.constants import SUPPORTED_APPIDS
from steam_trader.exceptions import UnsupportedAppID, UnknownItem
from steam_trader import (
    ClientAsync,
    Filters,
    Inventory,
    SellResult
)


logging.getLogger(__name__).addHandler(logging.NullHandler())

F = TypeVar('F', bound=Callable[..., Any])

def log(method: F) -> F:
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    async def wrapper(*args, **kwargs) -> Any:
        logger.debug(f'Entering: {method.__name__}')

        result = await method(*args, **kwargs)
        logger.info(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper


class ExtClientAsync(ClientAsync):
    """Данный класс представляет расширенную версию обычного клиента.

    Изменённые методы:
        get_inventory - Добавлена возможность указывать фильтр для отсеивания предметов.

    Новые методы:
        multi_sell - Аналог multi_buy. В отличие от него, возвращает последовательность из результатов продаж, а не один объект.
        set_trade_mode - Позволяет задать режим торговли. Данного метода нет в документации.
        get_price_range - Получить размах цен в истории покупок. Проверяет только последние 100 покупок.

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
        super().__init__(api_token, proxy=proxy, base_url=base_url, headers=headers)

    @log
    async def get_inventory(
            self,
            gameid: int,
            *,
            filters: Optional['Filters'] = None,
            status: Optional[Sequence[int]] = None
    ) -> 'Inventory':
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        EXT:
            Добавляен аргумент filters для отсеивания предметов.

        По умолчанию возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            filters (:class:`steam_trader.Filters`, optional): Фильтр для отсеивания предметов.
            status (Sequence[:obj:`int`], optional):
                Указывается, чтобы получить список предметов с определенным статусом.

                Возможные статусы:
                0 - В продаже
                1 - Принять
                2 - Передать
                3 - Ожидается
                4 - Заявка на покупку

                Если не указавать, вернётся список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

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

        result = await self._async_client.get(
            url,
            params=params,
            headers=self.headers
        )
        inventory = Inventory.de_json(result.json(), status, self)

        if filters is not None:
            tasks = [self.get_item_info(item.gid) for item in inventory.items]
            responses = await asyncio.gather(*tasks)

            new_items = []

            for i, item in enumerate(inventory.items):
                item_filters = responses[i].filters
                if filters.quality is not None:
                    required_filters_list = [_filter.id for _filter in filters.quality]
                    item_filters_list = [_filter.id for _filter in item_filters.quality]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.type is not None:
                    required_filters_list = [_filter.id for _filter in filters.type]
                    item_filters_list = [_filter.id for _filter in item_filters.type]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.used_by is not None:
                    required_filters_list = [_filter.id for _filter in filters.used_by]
                    item_filters_list = [_filter.id for _filter in item_filters.used_by]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.craft is not None:
                    required_filters_list = [_filter.id for _filter in filters.craft]
                    item_filters_list = [_filter.id for _filter in item_filters.craft]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.region is not None:
                    required_filters_list = [_filter.id for _filter in filters.region]
                    item_filters_list = [_filter.id for _filter in item_filters.region]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.genre is not None:
                    required_filters_list = [_filter.id for _filter in filters.genre]
                    item_filters_list = [_filter.id for _filter in item_filters.genre]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.mode is not None:
                    required_filters_list = [_filter.id for _filter in filters.mode]
                    item_filters_list = [_filter.id for _filter in item_filters.mode]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.trade is not None:
                    required_filters_list = [_filter.id for _filter in filters.trade]
                    item_filters_list = [_filter.id for _filter in item_filters.trade]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.rarity is not None:
                    required_filters_list = [_filter.id for _filter in filters.rarity]
                    item_filters_list = [_filter.id for _filter in item_filters.rarity]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue
                if filters.hero is not None:
                    required_filters_list = [_filter.id for _filter in filters.hero]
                    item_filters_list = [_filter.id for _filter in item_filters.hero]
                    if not any([required_filter in item_filters_list for required_filter in required_filters_list]):
                        continue

                new_items.append(item)

            inventory.items = new_items

        return inventory

    @log
    async def multi_sell(self, gameid: int, gid: int, price: float, count: int) -> Sequence['SellResult']:
        """Продать множество вещей из инвенторя с одним gid.

        Args:
            gameid (:obj:`int`): ID инвентаря из которого будет произходить продажа.
            gid (:obj:`int`): ID группы предметов.
            price (:obj:`int`): Цена для выставления на продажу.
            count (:obj:`int`): Количество предметов для продажи. Если число больше чем предметов в инвенторе,
                будут проданы те, что имеются.

        Returns:
            Sequence[:class:`steam_trader.SellResult`]: Последовательноасть с результатами продаж.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
            NoTradeLink: Отсутствует сслыка для обмена.
            IncorrectPrice: Неправильная цена заявки.
            ItemAlreadySold: Предмет уже продан или отстутствует.
            AuthenticatorError: Мобильный аутентификатор не подключён
                или с момента его подключения ещё не прошло 7 дней.
        """

        inventory = await self.get_inventory(gameid)
        tasks = []

        for item in inventory.items:
            if count == 0:
                break
            if item.gid == gid:
                tasks.append(self.sell(item.itemid, item.assetid, price))
                count -= 1

        results = await asyncio.gather(*tasks)

        return results

    @log
    async def set_trade_mode(self, state: int) -> 'TradeMode':
        """Задать режим торговли.

        Args:
            state (:obj:`int`): Режим торговли.
                0 - Торговля отключена.
                1 - Торговля включена.

        Returns:
            :class:`steam_trader.ext.TradeMode`: Режим торговли.

        Raises:
            ValueError: Недопустимое значение state.
        """

        if state not in range(2):
            raise ValueError(f'Недопустимое значение state :: {state}')

        url = self.base_url + 'startstoptrading/'
        result = await self._async_client.get(
            url,
            params={"state": state},
            headers=self.headers
        )
        return TradeMode.de_json(result.json(), self)

    @log
    async def get_price_range(self, gid: int, *, mode: LiteralString = 'sell') -> 'PriceRange':
        """Получить размах цен в истории покупок. Проверяет только последние 100 покупок.

        Args:
            gid (:obj:`int`): ID группы предметов.
            mode (:obj:`LiteralString`): Режим получения:
                'sell' - Цены запросов на продажу. Значение по умолчанию.
                'buy' - Цены запросов на покупку.
                'history' - Цены из истории продаж. Максимум 100 пунктов.

        Returns:
            :NamedTuple:`PriceRange(lowest: float, highest: float)`: Размах цен в истории покупок.

        Raises:
            InternalError: При выполнении запроса произошла неизвестная ошибка.
            ValueError: Указано недопустимое значение mode.
            UnknownItem: Отсутствуют предложения о продаже/покупке или отсутствует история продаж.
        """

        lowest = highest = None
        match mode:
            case 'sell':
                sell_offers = (await self.get_order_book(gid)).sell
                for item in sell_offers:
                    if lowest is None or item[0] < lowest:
                        lowest = item[0]
                    if highest is None or item[0] > highest:
                        highest = item[0]
            case 'buy':
                buy_offers = (await self.get_order_book(gid)).buy
                for item in buy_offers:
                    if lowest is None or item[0] < lowest:
                        lowest = item[0]
                    if highest is None or item[0] > highest:
                        highest = item[0]
            case 'history':
                sell_history = (await self.get_item_info(gid)).sell_history
                for item in sell_history:
                    if lowest is None or item.price < lowest:
                        lowest = item.price
                    if highest is None or item.price > highest:
                        highest = item.price
        if lowest is None or highest is None:
            raise UnknownItem('Отсутствуют предложения о продаже/покупке или отсутствует история продаж.')
        return PriceRange(float(lowest), float(highest))
