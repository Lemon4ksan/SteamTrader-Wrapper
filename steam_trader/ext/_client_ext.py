import httpx
from typing import Optional, List, LiteralString

from steam_trader import *
from steam_trader.constants import *
from steam_trader.exceptions import *


class ExtClient(Client):
    def __init__(self, api_token: str, *, base_url: str | None = None, headers: dict | None = None) -> None:
        super().__init__(api_token, base_url=base_url, headers=headers)

    def get_inventory(self, gameid: int, *, filters: Optional[Filters] = None, status: Optional[List[int]] = None):
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
        result = httpx.get(
            url,
            params={"gameid": gameid, 'status': status, "key": self.api_token},
            headers=self.headers
        ).json()

        inventory = Inventory.de_json(result, self)
        new_items = []

        for item in inventory.items:
            item_filters = self.get_item_info(item.gid).filters
            if filters.quality is not None:
                if not filters.quality[0].id == item_filters.quality[0].id:
                    continue
            if filters.type is not None:
                if not filters.type[0].id == item_filters.type[0].id:
                    continue
            if filters.used_by is not None:
                if not filters.used_by[0].id == item_filters.used_by[0].id:
                    continue
            if filters.craft is not None:
                if not filters.craft[0].id == item_filters.craft[0].id:
                    continue
            if filters.region is not None:
                if not filters.region[0].id == item_filters.region[0].id:
                    continue
            if filters.genre is not None:
                if not filters.genre[0].id == item_filters.genre[0].id:
                    continue
            if filters.mode is not None:
                if not filters.mode[0].id == item_filters.mode[0].id:
                    continue
            if filters.trade is not None:
                if not filters.trade[0].id == item_filters.trade[0].id:
                    continue
            if filters.rarity is not None:
                if not filters.rarity[0].id == item_filters.rarity[0].id:
                    continue
            if filters.hero is not None:
                if not filters.hero[0].id == item_filters.hero[0].id:
                    continue

            new_items.append(item)

        inventory.items = new_items
        return inventory
