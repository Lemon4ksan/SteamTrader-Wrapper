# Расширенный функционал
Библиотека предоставляет дополнительный функционал, который отсутствует в документации сайта.
Такой функционал будет полезен для оптимизации рутинных задач, или упрощения создания простых вещей.

## Инициализация
Инициализация расширенного клиента похожа на инициализацию обычного.
```python
from steam_trader.ext import ExtClient

client = ExtClient('Ваш токен')

# или

from steam_trader.ext import ExtClientAsync

client = ExtClientAsync('Ваш токен')
```

Расширенный клиент построен на основном клиенте и содержи все его методы.

## Изменённые методы

### get_inventory()
Добавлен аргумент filters для отсеивания предметов.
Для использования фильтра необходимо создать его экземпляр. Обязательно укажите id, другие поля опциональны.
```python
from steam_trader import Filters, Filter
from steam_trader.ext import ExtClient
from steam_trader.constants import *

client = ExtClient('Ваш токен')

filters = Filters(
            quality=[Filter(id=TF2_QUALITY_STRANGE), Filter(id=DOTA2_QUALITY_ELDER)],
            type=[Filter(id=TF2_TYPE_PRIMARY), Filter(id=DOTA2_TYPE_STICKER)],
            used_by=[Filter(id=TF2_CLASS_ENGINEER), Filter(id=TF2_CLASS_SCOUT)]
        )

filtered_inventory = client.get_inventory(TEAM_FORTRESS2_APPID, filters=filters)
```

!!! Заметка
    Запрос с фильрами на синхронном клиенте может занять до 2 минут.
    Если вы хотите ускорить выполнение, используйте асинхронную версию.

## Новые методы

### multi_sell()
Аналог multi_buy. Продаёт все предметы в инвентаре по gid. В отличие от него, возвращает последовательноасть из результатов продаж, а не один объект.
Если количество продаж больше чем соответствующих предметов в инвентаре, будут проданы те, что есть.
```python
from steam_trader.ext import ExtClient
from steam_trader.constants import TEAM_FORTRESS2_APPID

client = ExtClient('Ваш токен')

multi_sell_result = client.multi_sell(TEAM_FORTRESS2_APPID, 1220, 9.2, 10)
```

### set_trade_mode()
Задать режим торговли. Данного метода нет в документации сайта.

Режим 0 - торговля отключена. Режим 1 - торговля включена.
```python
from steam_trader.ext import ExtClient

client = ExtClient('Ваш токен')

trade_mode = client.set_trade_mode(1)
```

### get_price_range()
Получить размах цен.

Режим получения:
'sell' - Цены запросов на продажу. Значение по умолчанию. 
'buy' - Цены запросов на покупку. 
'history' - Цены из истории продаж. Максимум 100 пунктов.

```python
from steam_trader.ext import ExtClient

client = ExtClient('Ваш токен')

price_range = client.get_price_range(1220, mode='sell')
#  PriceRange(lowest=1.04, highest=10)
```