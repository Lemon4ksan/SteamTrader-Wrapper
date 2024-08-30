import httpx
import logging
import functools
from typing import Optional, Sequence, TypeVar, Callable, Any

from ._misc import TradeMode

from steam_trader.constants import SUPPORTED_APPIDS
from steam_trader.exceptions import UnsupportedAppID
from steam_trader import (
    Client,
    Filters,
    Inventory,
    SellResult
)


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


class ExtClient(Client):
    """Данный класс представляет расширенную версию обычного клиента.

    Изменённые методы:
        get_inventory - Добавлена возможность указывать фильтр для отсеивания предметов
        (очень медленно на синхронном клиенте).

    Новые методы:
        multi_sell - Аналог multi_buy. В отличие от него, возвращает последовательноасть из результатов продаж, а не один объект.
        set_trade_mode - Позволяет задать режим торговли. Данного метода нет в документации.

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
    def get_inventory(
            self,
            gameid: int,
            *,
            filters: Optional['Filters'] = None,
            status: Optional[Sequence[int]] = None
    ) -> Optional['Inventory']:
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
            :class:`steam_trader.Inventory`, optional: Инвентарь клиента, включая заявки на покупку и купленные предметы.

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
        inventory = Inventory.de_json(result, status, self)

        if filters is not None:
            logging.warning('Вы используете синхронный клиент. Запрос с фильтрами может занять до 2 минут. Если хотите ускорить время, используйте асинхронную версию.')
            new_items = []

            for item in inventory.items:
                item_filters = self.get_item_info(item.gid).filters
                if filters.quality is not None:
                    requred_filters_list = [_filter.id for _filter in filters.quality]
                    item_filters_list = [_filter.id for _filter in item_filters.quality]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.type is not None:
                    requred_filters_list = [_filter.id for _filter in filters.type]
                    item_filters_list = [_filter.id for _filter in item_filters.type]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.used_by is not None:
                    requred_filters_list = [_filter.id for _filter in filters.used_by]
                    item_filters_list = [_filter.id for _filter in item_filters.used_by]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.craft is not None:
                    requred_filters_list = [_filter.id for _filter in filters.craft]
                    item_filters_list = [_filter.id for _filter in item_filters.craft]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.region is not None:
                    requred_filters_list = [_filter.id for _filter in filters.region]
                    item_filters_list = [_filter.id for _filter in item_filters.region]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.genre is not None:
                    requred_filters_list = [_filter.id for _filter in filters.genre]
                    item_filters_list = [_filter.id for _filter in item_filters.genre]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.mode is not None:
                    requred_filters_list = [_filter.id for _filter in filters.mode]
                    item_filters_list = [_filter.id for _filter in item_filters.mode]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.trade is not None:
                    requred_filters_list = [_filter.id for _filter in filters.trade]
                    item_filters_list = [_filter.id for _filter in item_filters.trade]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.rarity is not None:
                    requred_filters_list = [_filter.id for _filter in filters.rarity]
                    item_filters_list = [_filter.id for _filter in item_filters.rarity]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue
                if filters.hero is not None:
                    requred_filters_list = [_filter.id for _filter in filters.hero]
                    item_filters_list = [_filter.id for _filter in item_filters.hero]
                    if not any([required_filter in item_filters_list for required_filter in requred_filters_list]):
                        continue

                new_items.append(item)

            inventory.items = new_items

        return inventory

    @log
    def multi_sell(self, gameid: int, gid: int, price: float, count: int) -> Sequence[Optional['SellResult']]:
        """Продать множество вещей из инвенторя с одним gid.

        Args:
            gameid (:obj:`int`): ID инвентаря из которого будет произходить продажа.
            gid (:obj:`int`): ID группы предметов.
            price (:obj:`int`): Цена для выставления на продажу.
            count (:obj:`int`): Количество предметов для продажи. Если число больше чем предметов в инвенторе,
                будут проданы те, что имеются.

        Returns:
            Sequence[:class:`steam_trader.SellResult, optional`]: Последовательноасть с результатами продаж.

        Raises:
            OfferCreationFail: При создании заявки произошла неизвестная ошибка.
            UnknownItem: Неизвестный предмет.
            NoTradeLink: Отсутствует сслыка для обмена.
            IncorrectPrice: Неправильная цена заявки.
            ItemAlreadySold: Предмет уже продан или отстутствует.
            AuthenticatorError: Мобильный аутентификатор не подключён
                или с момента его подключения ещё не прошло 7 дней.
        """

        inventory = self.get_inventory(gameid)
        results = []

        for item in inventory.items:
            if count == 0:
                break
            if item.gid == gid:
                results.append(self.sell(item.itemid, item.assetid, price))
                count -= 1

        return results

    @log
    def set_trade_mode(self, state: int) -> Optional['TradeMode']:
        """Задать режим торговли. Данного метода нет в документации.

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
        result = (self._httpx_client or httpx).get(
            url,
            params={"state": state},
            headers=self.headers
        ).json()
        return TradeMode.de_json(result, self)
