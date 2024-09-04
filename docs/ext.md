# Ext клиент

## `ExtClient`

Одинаково для синхронного и асинхронного клиента.

Имеет все методы основного клиента.

::: steam_trader.ext.ExtClient

> **Аргументы**

> * **api_token** `str`: Уникальный ключ для аутентификации.
> * **proxy** `str`, optional: Прокси для запросов. Для работы необходимо использовать контекстный менеджер with.
> * **base_url** `str`, optional: Ссылка на API Steam Trader.
> * **headers** `dict`, optional: Словарь, содержащий сведения об устройстве, с которого выполняются запросы. Используется при каждом запросе на сайт.

`api_token`
> Уникальный ключ для аутентификации.
> 
> **Тип**: `str`

`proxy`, optional
> Прокси для запросов. Для работы необходимо использовать контекстный менеджер with.
> 
> **Тип**: `str`

`base_url`, optional
> Ссылка на API Steam Trader.
> 
> **Тип**: `str`

`headers`, optional
> Словарь, содержащий сведения об устройстве, с которого выполняются запросы.
> 
> **Тип**: `dict`

**Использование**:
```python
from steam_trader.ext import ExtClient

client = ExtClient('Ваш токен')
...

# или

with client:
    ...
```

```python
from steam_trader.ext import ExtClientAsync

client = ExtClientAsync('Ваш токен')

async def main():
    async with client:
        ...
```
---

#### `get_inventory`(*self, gameid, \*, filters=None, status=None*)
> Получить инвентарь клиента, включая заявки на покупку и купленные предметы.
> По умолчанию возвращает список предметов из инвентаря Steam, которые НЕ выставлены на продажу.
> 
> **Аргументы**
> 
> * **gameid** `int`: AppID приложения в Steam.
> * **filters** *class* [`Filters`](dataclasses.md#filters), optional: Фильтр для отсеивания предметов.
> * **status** Sequnce[ `int` ], optional: Указывается, чтобы получить список предметов с определенным статусом.
    - 0 - В продаже
    - 1 - Принять
    - 2 - Передать
    - 3 - Ожидается
    - 4 - Заявка на покупку
> 
> **Возвращает**: *class* [Inventory](dataclasses.md#inventory), optional

#### `multi_sell`(*self, gameid, gid, price, count*)
> Продать множество вещей из инвенторя с одним gid.
> 
> **Аргументы**
> 
> * **gameid** `int`: AppID приложения в Steam.
> * **gid** `int`: ID группы предметов.
> * **price** `float`: Цена для выставления на продажу.
> * **count**  `int`: Количество предметов для продажи. Если число больше чем предметов в инвенторе, будут проданы те, что имеются.
>
> *Возвращает*: Sequence[ *class* [`SellResult`](dataclasses.md#sellresult), optional ]

#### `set_trade_mode`(*self, state*)
> Задать режим торговли.
> 
> **Аргументы**
> 
> * **state** `int`: Режим торговли.
    - 0 - Торговля отключена.
    - 1 - Торговля включена.
>
> *Возвращает*: *class* [`TradeMode`](#trademode)

## Датаклассы

### `TradeMode`

[//]: # (::: steam_trader.ext.TradeMode)
> Класс, представляющий режим торговли.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`state`
> Режим обычной торговли.
> 
> **Тип**: `bool`

`p2p`
> Режим p2p торговли.
> 
> **Тип**: `bool`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]