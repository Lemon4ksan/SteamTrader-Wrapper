import asyncio
from typing import Optional, LiteralString, Sequence

from steam_trader import *
from steam_trader.constants import *
from steam_trader.exceptions import *


class ExtClientAsync(ClientAsync):
    """Данный класс представляет расширенную версию обычного клиента.

    Изменённые методы:
        get_inventory - Добавлена возможность указывать фильтр для отсеивания предметов
        (очень медленно на синхронном клиенте).

    Новые методы:
        multi_sell - Аналог multi_buy. В отличие от него, возвращает последовательность из результатов продаж, а не один объект.
    """

    def __init__(self, api_token: str, *, base_url: str | None = None, headers: dict | None = None) -> None:
        super().__init__(api_token, base_url=base_url, headers=headers)

    async def get_inventory(self, gameid: int, *, filters: Optional['Filters'] = None, status: Optional[Sequence[int]] = None):
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        EXT:
            Добавляен аргумент filters для отсеивания предметов.

        По умолчанию (то есть всегда) возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Note:
            Аргумент status не работает.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            filters (:class:`steam_trader.Filters`, optional): Фильтр для отсеивания предметов.
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
        result = result.json()
        inventory = Inventory.de_json(result, self)

        if filters is not None:
            tasks = [self.get_item_info(item.gid) for item in inventory.items]
            responses = await asyncio.gather(*tasks)

            new_items = []

            for i, item in enumerate(inventory.items):
                item_filters = responses[i].filters
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

    async def multi_sell(self, gameid: int, gid: int, price: float, count: int) -> Sequence[Optional['SellResult']]:
        """Продать множество вещей из инвенторя с одним gid.

        Args:
            gameid (:obj:`int`): ID инвентаря из которого будет произходить продажа.
            gid (:obj:`int`): ID группы предметов.
            price (:obj:`int`): Цена для выставления на продажу.
            count (:obj:`int`): Количество предметов для продажи. Если число больше чем предметов в инвенторе,
                будут проданы те, что имеются.

        Returns:
            Sequence[:class:`steam_trader.SellResult, optional`]: Последовательноасть с результатами продаж.
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
