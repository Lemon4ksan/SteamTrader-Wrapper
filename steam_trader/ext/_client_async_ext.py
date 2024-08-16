import httpx
import asyncio
from typing import Optional, List, LiteralString, Sequence

from steam_trader import *
from steam_trader.constants import *
from steam_trader.exceptions import *


class ExtClientAsync(ClientAsync):
    def __init__(self, api_token: str, *, base_url: str | None = None, headers: dict | None = None) -> None:
        super().__init__(api_token, base_url=base_url, headers=headers)

    async def get_inventory(self, gameid: int, *, filters: Optional[Filters] = None, status: Optional[List[int]] = None):
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        EXT:
            Добавляет аргумент filters для отсеивания предметов.

        По умолчанию (то есть всегда) возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Note:
            Аргумент status не работает.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            filters (:class:`steam_trader.Filters`): Фильтр для отсеивания предметов.
            status (:list:`int`, optional): Указывается, чтобы получить список предметов с определенным статусом.

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

        tasks = [self.get_item_info(item.gid) for item in inventory.items]
        responses: Sequence['ItemInfo'] = await asyncio.gather(*tasks)

        new_items = []

        for i, response in enumerate(responses):

            if filters.quality is not None:
                if not filters.quality[0].id == response.filters.quality[0].id:
                    continue
            if filters.type is not None:
                if not filters.type[0].id == response.filters.type[0].id:
                    continue
            if filters.used_by is not None:
                if not filters.used_by[0].id == response.filters.used_by[0].id:
                    continue
            if filters.craft is not None:
                if not filters.craft[0].id == response.filters.craft[0].id:
                    continue
            if filters.region is not None:
                if not filters.region[0].id == response.filters.region[0].id:
                    continue
            if filters.genre is not None:
                if not filters.genre[0].id == response.filters.genre[0].id:
                    continue
            if filters.mode is not None:
                if not filters.mode[0].id == response.filters.mode[0].id:
                    continue
            if filters.trade is not None:
                if not filters.trade[0].id == response.filters.trade[0].id:
                    continue
            if filters.rarity is not None:
                if not filters.rarity[0].id == response.filters.rarity[0].id:
                    continue
            if filters.hero is not None:
                if not filters.hero[0].id == response.filters.hero[0].id:
                    continue

            new_items.append(inventory.items[i])

        inventory.items = new_items
        return inventory
