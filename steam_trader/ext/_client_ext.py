import httpx
from typing import Optional, List, LiteralString

from steam_trader import *
from steam_trader.constants import *
from steam_trader.exceptions import *


class ExtClient(Client):
    def __init__(self, api_token: str, *, base_url: str | None = None, headers: dict | None = None) -> None:
        """Данный класс представляет расширенную версию обычного клиента.

        Изменённые методы:
            get_inventory - Добавлена возможность указывать фильтр для отсеивания предметов
            (очень медленно на синхронном клиенте).
        """
        super().__init__(api_token, base_url=base_url, headers=headers)

    def get_inventory(self, gameid: int, *, filters: Optional['Filters'] = None, status: Optional[List[int]] = None) -> Optional['Inventory']:
        """Получить инвентарь клиента, включая заявки на покупку и купленные предметы.

        EXT:
            Добавляен аргумент filters для отсеивания предметов.

        По умолчанию (то есть всегда) возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.

        Note:
            Аргумент status не работает.

        Args:
            gameid (:obj:`int`): AppID приложения в Steam.
            filters (:class:`steam_trader.Filters`, optional): Фильтр для отсеивания предметов.
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
