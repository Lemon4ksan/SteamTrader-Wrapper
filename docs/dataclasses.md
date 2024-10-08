# Датаклассы

Данные классы (кроме фильтров) не должны создаваться пользователем.

## Продажа

### `SellResult`

::: steam_trader.SellResult
> Класс, представляющий информацию о выставленном на продажу предмете.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`id`
> ID продажи.
> 
> **Тип**: `int`

`position`
> Позиция предмета в очереди.
> 
> **Тип**: `int`

`fast_execute`
> Был ли предмет продан моментально.
> 
> **Тип**: `bool`

`nc`
> Идентификатор для бескомиссионной продажи предмета.
> 
> **Тип**: `str`

`price`
> Цена, за которую был продан предмет с учетом комиссии.
> Указывается, если 'fast_execute' = True
> 
> **Тип**: `float`, optional

`commission`
> Размер комиссии в процентах, за которую был продан предмет.
> Указывается, если 'fast_execute' = True
> 
> **Тип**: `float`, optional

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Покупка

### `BuyResult`

::: steam_trader.BuyResult
> Класс, представляющий результат покупки.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`id`
> ID покупки.
> 
> **Тип**: `int`

`gid`
> ID группы предметов.
> 
> **Тип**: `int`

`itemid`
> Униклаьный ID купленного предмета.
> 
> **Тип**: `int`

`price`
> Цена, за которую был куплен предмет с учётом скидки.
> 
> **Тип**: `float`

`new_price`
> Новая цена лучшего предложения о продаже для варианта покупки Commodity, 
> если у группы предметов ещё имеются предложения о продаже. Для остальных вариантов покупки будет 0
> 
> **Тип**: `float`

`discount`
> Размер скидки в процентах, за которую был куплен предмет.
> 
> **Тип**: `float`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `BuyOrderResult`

::: steam_trader.BuyOrderResult
> Класс, представляющий результат запроса на покупку.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`executed`
> Количество исполненных заявок.
> 
> **Тип**: `int`

`placed`
> Количество размещённых на маркет заявок.
> 
> **Тип**: `int`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `MultiBuyResult`

::: steam_trader.MultiBuyResult
> Класс, представляющий результат мульти-покупки.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`balance`
> Баланс после покупки предметов. Указывается если 'success' = True
> 
> **Тип**: `float`, optional

`spent`
> Сумма потраченных средств на покупку предметов. Указывается если 'success' = True
> 
> **Тип**: `float`, optional

`orders`
> Последовательность купленных предметов. Указывается если 'success' = True
> 
> **Тип**: Sequence[ *class* [`MultiBuyOrder`](#multibuyitem) ], optional

`left`
> Сколько предметов по этой цене осталось. Если операция прошла успешно, всегда равен 0.
> 
> **Тип**: `int`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Редактирование

### `EditPriceResult`

::: steam_trader.EditPriceResult
> Класс, представляющий результат запроса на изменение цены.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`type`
> Тип заявки. 0 - продажа, 1 - покупка.
> 
> **Тип**: `int`

`position`
> Позиция предмета в очереди.
> 
> **Тип**: `int`

`fast_execute`
> Был ли предмет продан/куплен моментально.
> 
> **Тип**: `bool`

`new_id`
> Новый ID заявки. Указывается, если 'fast_execute' = True.
> Новый ID присваивается только заявкам на ПОКУПКУ и только в случае редактирования уже имеющейся заявки.
> 
> **Тип**: `int`, optional

`price`
> Цена, за которую был продан/куплен предмет с учётом комиссии/скидки.
> Указывается, если 'fast_execute' = True.
> 
> **Тип**: `float`, optional

`percent`
> Размер комиссии/скидки в процентах, за которую был продан/куплен предмет.
> Указывается, если 'fast_execute' = true.
> 
> **Тип**: `float`, optional

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `DeleteItemResult`

::: steam_trader.DeleteItemResult
> Класс, представляющий результат запроса снятия предмета с продажи/заявки на покупку.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`has_ex`
> Есть ли доступный обмен на сайте.
> 
> **Тип**: `bool`

`has_bot_ex`
> Есть ли доступный обмен с ботом.
> 
> **Тип**: `bool`

`has_p2p_ex`
> Есть ли доступный P2P обмен.
> 
> **Тип**: `bool`

`total_fines`
> Общее количество штрафных баллов.
> 
> **Тип**: `int`

`fine_date`
> Дата снятия штрафных баллов. Если None - штрафных баллов нет.
> 
> **Тип**: `int`, optional

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `GetDownOrdersResult`

::: steam_trader.GetDownOrdersResult
> Класс, представляющий результат снятия всех заявок на продажу/покупку.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`count`
> Количество удалённых предложений.
> 
> **Тип**: `int`

`ids`
> Список из ID удалённых предложений.
> 
> **Тип**: Sequence[ int ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Обмен

### `ItemsForExchange`

::: steam_trader.ItemsForExchange
> Класс, представляющий предметы для обмена с ботом.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`items`
> Последовательность предметов для обмена с ботом.
> 
> **Тип**: Sequence[ *class* [`ItemForExchange`](#itemforexchange) ]

`description`
> Описания предметов для обмена с ботом. Ключ - itemid предмета.
> 
> **Тип**: dict[ int, *class* `TradeDescription` ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `ExchangeResult`

::: steam_trader.ExchangeResult
> Класс, представляющий результат инициализации обмена с ботом.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`offer_id`
> ID обмена в Steam.
> 
> **Тип**: `int`

`code`
> Код проверки обмена.
> 
> **Тип**: `str`

`bot_steamid`
> SteamID бота, который отправил обмен.
> 
> **Тип**: `int`

`bot_nick`
> Ник бота.
> 
> **Тип**: `str`

`items`
> Cписок предметов для обмена с ботом.
> 
> **Тип**: Sequence[ *class* [`ExchangeItem`](#exchangeitem) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `ExchangeP2PResult`
> Класс, представляющий результат инициализации p2p обмена.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`send`
> Массив с данными для создания нового обмена в Steam.
> 
> **Тип**: Sequence[ *class* [`P2PSendObject`](#p2psendobject) ]

`recieve`
> Массив с данными для принятия обмена.
> 
> **Тип**: Sequence[ *class* [`P2PRecieveObject`](#p2preceiveobject) ]

`confirm`
> Массив с данными для подтверждения обмена в мобильном аутентификаторе.
> 
> **Тип**: Sequence[ *class* [`P2PConfirmObject`](#p2pconfirmobject) ]

`cancel`
> Массив из ID обменов, которые нужно отменить.
> 
> **Тип**: Sequence[ `str` ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Информация

### `MinPrices`

::: steam_trader.MinPrices
> Класс, представляющий минимальную/максимальную цену на предмет.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`market_price`
> Минимальная цена продажи. Может быть пустым.
> 
> **Тип**: `float`, optional

`buy_price`
> Максимальная цена покупки. Может быть пустым.
> 
> **Тип**: `float`, optional

`steam_price`
> Минимальная цена в Steam. Может быть пустым.
> 
> **Тип**: `float`, optional

`count_sell_offers`
> Количество предложений о продаже.
> 
> **Тип**: `int`, optional

`count_buy_offers`
> Количество предложений о покупке.
> 
> **Тип**: `int`, optional

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `ItemInfo`

::: steam_trader.ItemInfo
> Класс, представляющий информацию о группе предметов на сайте.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`name`
> Локализованное (переведённое) название предмета.
> 
> **Тип**: `str`

`hash_name`
> Параметр 'market_hash_name' в Steam.
> 
> **Тип**: `float`

`type`
> Тип предмета (из Steam).
> 
> **Тип**: `str`

`gameid`
> AppID приложения в Steam.
> 
> **Тип**: `int`

`contextid`
> ContextID приложения в Steam.
> 
> **Тип**: `int`

`color`
> Hex код цвета предмета (из Steam).
> 
> **Тип**: `str`

`small_image`
> Абсолютная ссылка на маленькое изображение предмета.
> 
> **Тип**: `str`

`large_image`
> Абсолютная ссылка на большое изображение предмета.
> 
> **Тип**: `str`

`marketable`
> Параметр 'marketable' в Steam.
> 
> **Тип**: `bool`

`tradable`
> Параметр 'tradable' в Steam.
> 
> **Тип**: `bool`

`description`
> Локализованное (переведённое) описание предмета.
> 
> **Тип**: `str`

`market_price`
> Минимальная цена продажи. Может быть пустым.
> 
> **Тип**: `float`, optional

`buy_price`
> Максимальная цена покупки. Может быть пустым.
> 
> **Тип**: `float`, optional

`steam_price`
> Минимальная цена в Steam. Может быть пустым.
> 
> **Тип**: `float`, optional

`filters`
> Фильтры, используемые для поиска на сайте.
> 
> **Тип**: *class* `Filters`, optional

`sell_offers`
> Последовательность с предложениями о продаже.
> 
> **Тип**: Sequence[ *class* [`SellOffer`](#selloffer) ]

`buy_offers`
> Последовательность с предложениями о покупке.
> 
> **Тип**: Sequence[ *class* [`BuyOffer`](#buyoffer) ]

`sell_history`
> Последовательность истории продаж.
> 
> **Тип**: Sequence[ *class* [`SellHistoryItem`](#sellhistoryitem) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `OrderBook`

::: steam_trader.OrderBook
> Класс, представляющий заявоки о покупке/продаже предмета.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`sell`
> Сгруппированный по цене список заявок на продажу.
> Каждый элемент в списке является массивом, где первый элемент - это цена, а второй - количество заявок.
> 
> **Тип**: Sequence[ Sequence[ `int`, `int` ] ]

`buy`
> Сгруппированный по цене список заявок на покупку.
> Каждый элемент в списке является массивом, где первый элемент - это цена, а второй - количество заявок.
> 
> **Тип**: Sequence[ Sequence[ `int`, `int` ] ]

`total_sell`
> Количество всех заявок на продажу.
> 
> **Тип**: `int`, optional

`total_buy`
> Количество всех заявок на покупку.
> 
> **Тип**: `int`, optional

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Аккаунт

### `WebSocketToken`
> Незадокументированно

### `Inventory`

::: steam_trader.Inventory
> Класс, представляющий инвентарь клиента.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`count`
> Количество всех предметов в инвентаре Steam.
> 
> **Тип**: `int`

`gameid`
> AppID игры к которой принадлежит инвентарь.
> 
> **Тип**: `int`

`last_update`
> Timestamp последнего обновления инвентаря.
> 
> **Тип**: `int`

`items`
> Последовательность с предметами в инвентаре.
> 
> **Тип**: Sequence[ *class* [`InventoryItem`](#inventoryitem) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `BuyOrders`

::: steam_trader.BuyOrders
> Класс, представляющий ваши запросы на покупку.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`data`
> Последовательность запросов на покупку.
> 
> **Тип**: Sequence[ *class* [`BuyOrder`](#buyorder) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `Discounts`

::: steam_trader.Discounts
> Класс, представляющий комиссии/скидки на игры, доступные на сайте.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`data`
> Словарь, содержащий комисии/скидки.
> 
> **Тип**: dict[ `int`, *class* [`Discount`](#discount) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `OperationsHistory`

::: steam_trader.OperationsHistory
> Класс, представляющий истории операций, произведённых на сайте.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`data`
> Последовательность историй операций.
> 
> **Тип**: Sequence[ *class* [`OperationsHistoryItem`](#operationshistoryitem) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `InventoryState`

::: steam_trader.InventoryState
> Класс, представляющий текущий статус инвентаря.

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`updating_now`
> Инвентарь обновляется в данный момент.
> 
> **Тип**: `bool`

`last_update`
> Timestamp, когда последний раз был обновлён инвентарь.
> 
> **Тип**: `int`

`items_in_cache`
> Количество предметов в инвентаре.
> 
> **Тип**: `int`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

### `AltWebSocket`

::: steam_trader.AltWebSocket
> Класс, представляющий запрос альтернативным WebSocket.

`success`
> Результат запроса. Если false, сообщений в поле messages не будет, при этом соединение будет поддержано.
> 
> **Тип**: `bool`

`messages`
> Последовательность с WebSocket сообщениями.
> 
> **Тип**: Sequence[ *class* [`AltWebSocketMessage`](#altwebsocketmessage) ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* [`Client`](client.md#client), *class* [`ClientAsync`](client.md#client), `None` ]

## Фильтры

### `Filters`

::: steam_trader.Filters
> Класс, представляющий фильтры, используемые для поиска на сайте.

`quality`
> Качество предмета (TF2, DOTA2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`type`
> Тип предмета (TF2, DOTA2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`used_by`
> Класс, который использует предмет (TF2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`craft`
> Информация о карфте (TF2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`region`
> Регион игры (SteamGift).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`genre`
> Жанр игры (SteamGift).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`mode`
> Тип игры, взаимодействие с Steam (SteamGift).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`trade`
> Информация об обмене (SteamGift).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`rarity`
> Редкость предмета (DOTA2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

`hero`
> Герой, который использует предмет (DOTA2).
> 
> **Тип**: Sequence[ *class* [`Filter`](#filter) ], optional

### `Filter`

::: steam_trader.Filter
> Класс, представляющий фильтр.

`id`
> ID данного фильтра, может быть пустым. Если вы создаёте класс вручную, то обязательно укажите этот параметр.
> 
> **Тип**: `int`, optional

`title`
> Тайтл данного фильтра, может быть пустым.
> 
> **Тип**: `str`, optional

`color`
> Цвет данного фильтра, может быть пустым.
> 
> **Тип**: `str`, optional

## Подклассы

### `MultiBuyOrder`

::: steam_trader.MultiBuyOrder
> Класс, представляющий предмет из запроса на мульти-покупку

`id`
> ID заявки.
> 
> **Тип**: `int`

`itemid`
> Уникальный ID предмета.
> 
> **Тип**: `int`

`price`
> Цена, за которую был куплен предмет с учётом скидки.
> 
> **Тип**: `float`

### `ItemForExchange`

::: steam_trader.ItemForExchange
> Класс, представляющий информацию о предмете для передачи/получения боту.

`id`
> ID покупки/продажи.
> 
> **Тип**: `int`

`assetid`
> AssetID предмета в Steam.
> 
> **Тип**: `int`

`gameid`
> AppID приложения в Steam.
> 
> **Тип**: `int`

`contextid`
> ContextID приложения в Steam.
> 
> **Тип**: `int`

`classid`
> Параметр ClassID в Steam.
> 
> **Тип**: `int`

`instanceid`
> Параметр InstanceID в Steam.
> 
> **Тип**: `int`

`gid`
> ID группы предметов.
> 
> **Тип**: `int`

`itemid`
> Уникальный ID предмета.
> 
> **Тип**: `int`

`price`
> Цена предмета, за которую купили/продали, без учета комиссии/скидки.
> 
> **Тип**: `float`

`currency`
> Валюта покупки/продажи.
> 
> **Тип**: `int`

`timer`
> Cколько времени осталось до передачи боту/окончания гарантии.
> 
> **Тип**: `int`

`asset_type`
> Значение 0 - этот предмет для передачи боту. Значение 1 - для приёма предмета от бота.
> 
> **Тип**: `int`

`percent`
> Размер комиссии/скидки в процентах, за которую был продан/куплен предмет.
> 
> **Тип**: `float`

`steam_item`
> Присутствует ли предмет в вашем инвентаре Steam.
> 
> **Тип**: `bool`

### `ExchangeItem`

::: steam_trader.ExchangeItem
> Класс, представляющий предмет, на который был отправлен обмен.

`id`
> ID покупки/продажи.
> 
> **Тип**: `int`

`assetid`
> AssetID предмета в Steam.
> 
> **Тип**: `int`

`gameid`
> AppID приложения в Steam.
> 
> **Тип**: `int`

`contextid`
> ContextID приложения в Steam.
> 
> **Тип**: `int`

`classid`
> Параметр ClassID в Steam.
> 
> **Тип**: `int`

`instanceid`
> Параметр InstanceID в Steam.
> 
> **Тип**: `int`

`type`
> Значение 0 - этот предмет для передачи боту. Значение 1 - для приёма предмета от бота.
> 
> **Тип**: `int`

`itemid`
> Уникальный ID предмета.
>
> **Тип**: `int`

`gid`
> ID группы предметов.
>
> **Тип**: `int`

`price`
> Цена, за которую предмет был куплен/продан с учётом скидки/комиссии.
> 
> **Тип**: `float`

`currency`
> Валюта покупки/продажи.
> 
> **Тип**: `int`

`percent`
> Размер комиссии/скидки в процентах, за которую был продан/куплен предмет.
> 
> **Тип**: `float`

### `P2PTradeOffer`

[//]: # (::: steam_trader.P2PTradeOffer)
> Класс, представляющий данные для совершения p2p трейда. Незадокументированно.

### `P2PSendObject`

::: steam_trader.P2PSendObject
> Класс, представляющий ссылку на p2p обмен и сам обмен.

`trade_link`
> Ссылка для p2p обмена.
> 
> **Тип**: `str`

`trade_offer`
> Параметры для POST запроса (https://steamcommunity.com/tradeoffer/new/send) при создании обмена в Steam. 
> Вместо {sessionid} нужно указывать ID своей сессии в Steam.
> 
> **Тип**: *class* [`P2PTradeOffer`](#p2ptradeoffer)

### `P2PReceiveObject`

::: steam_trader.P2PReceiveObject
> Класс, представляющий массив с данными для принятия обмена.

`offerid`
> ID обмена в Steam.
> 
> **Тип**: `int`

`code`
> Код проверки обмена.
> 
> **Тип**: `str`

`items`
> Ссылка для p2p обмена.
> 
> **Тип**: Sequence[ *class* [`ExchangeItem`](#exchangeitem)]

`partner_steamid`
> SteamID покупателя.
> 
> **Тип**: `int`

### `P2PConfirmObject`

::: steam_trader.P2PConfirmObject
> Класс, представляющий массив с данными для подтверждения обмена в мобильном аутентификаторе.

`offerid`
> ID обмена в Steam.
> 
> **Тип**: `int`

`code`
> Код проверки обмена.
> 
> **Тип**: `str`

`partner_steamid`
> SteamID покупателя.
> 
> **Тип**: `int`


### `SellOffer`

::: steam_trader.SellOffer
> Класс, представляющий информацию о предложении продажи.

`id`
> ID заявки.
> 
> **Тип**: `int`

`classid`
> ClassID предмета в Steam.
> 
> **Тип**: `int`

`instanceid`
> InstanceID предмета в Steam.
> 
> **Тип**: `int`

`itemid`
> Уникальный ID предмета.
> 
> **Тип**: `int`

`price`
> Цена предложения о покупке/продаже.
> 
> **Тип**: `float`

`currency`
> Валюта покупки/продажи.
> 
> **Тип**: `int`

### `BuyOffer`

::: steam_trader.BuyOffer
> Класс, представляющий информацию о предложении продажи.

`id`
> ID заявки.
> 
> **Тип**: `int`

`price`
> Цена предложения о покупке/продаже.
> 
> **Тип**: `float`

`currency`
> Валюта покупки/продажи.
> 
> **Тип**: `int`

### `SellHistoryItem`

::: steam_trader.SellHistoryItem
> Класс, представляющий информацию о предмете в истории продаж.

`date`
> Timestamp времени продажи.
> 
> **Тип**: `int`

`price`
> Цена предложения о покупке/продаже.
> 
> **Тип**: `float`

### `BuyOrder`

::: steam_trader.BuyOrder
> Класс, представляющий информацию о запросе на покупку.

`id`
> ID заявки на покупку.
> 
> **Тип**: `int`

`gid`
> ID группы предметов.
> 
> **Тип**: `int`

`gameid`
> AppID приложения в Steam.
> 
> **Тип**: `int`

`hash_name`
> Параметр market_hash_name в Steam.
> 
> **Тип**: `str`

`date`
> Timestamp подачи заявки.
> 
> **Тип**: `int`

`price`
> Предлагаемая цена покупки без учёта скидки.
> 
> **Тип**: `float`

`currency`
> Валюта, значение 1 - рубль.
> 
> **Тип**: `int`

`position`
> Позиция заявки в очереди.
> 
> **Тип**: `int`

### `InventoryItem`

::: steam_trader.InventoryItem
> Класс, представляющий предмет в инвентаре.

`id`
> ID заявки на покупку/продажу. Может быть пустым.
> 
> **Тип**: `int`, optional

`assetid`
> AssetID предмета в Steam. Может быть пустым.
> 
> **Тип**: `int`, optional

`gid`
> ID группы предметов.
> 
> **Тип**: `int`

`itemid`
> Уникальный ID предмета.
> 
> **Тип**: `int`

`price`
> Цена, за которую предмет был выставлен/куплен/продан предмет без учёта скидки/комиссии. Может быть пустым.
> 
> **Тип**: `float`, optional

`price`
> Валюта, за которую предмет был выставлен/куплен/продан. Значение 1 - рубль. Может быть пустым.
> 
> **Тип**: `int`, optional

`timer`
> Время, которое доступно для приема/передачи этого предмета. Может быть пустым.
> 
> **Тип**: `int`, optional

`type`
> Тип предмета. 0 - продажа, 1 - покупка. Может быть пустым.
> 
> **Тип**: `int`, optional

`status`
> Статус предмета.
>
* 2 - Предмет в инвентаре Steam не выставлен на продажу.
* 0 - Предмет выставлен на продажу или выставлена заявка на покупку. Для различия используется поле type.
* 1 - Предмет был куплен/продан и ожидает передачи боту или P2P способом. Для различия используется поле type.
* 2 - Предмет был передан боту или P2P способом и ожидает приёма покупателем.
* 6 - Предмет находится в режиме резервного времени. На сайте отображается как "Проверяется" после истечения времени на передачу боту или P2P способом.

> **Тип**: `int`

`position`
> Позиция предмета в списке заявок на покупку/продажу. Может быть пустым.
> 
> **Тип**: `int`, optional

`nc`
> ID заявки на продажу для бескомиссионной ссылки. Может быть пустым.
> 
> **Тип**: `int`, optional

`percent`
> Размер скидки/комиссии в процентах, с которой был куплен/продан предмет. Может быть пустым.
> 
> **Тип**: `float`, optional

`steam_item`
> Присутствует ли предмет в вашем инвентаре Steam.
> 
> **Тип**: `bool`

`nm`
> Незадокументированно.
> 
> **Тип**: `bool`

### `Discount`

::: steam_trader.Discount
> Класс, представляющий информацию о комиссии/скидке в определённой игре.

`total_buy`
> Cколько денег потрачено на покупки.
> 
> **Тип**: `float`

`total_sell`
> Cколько денег получено с продажи предметов.
> 
> **Тип**: `float`

`discount`
> Cкидка на покупку. Величина в %.
> 
> **Тип**: `float`

`percent`
> Комиссия на продажу. Величина в %.
> 
> **Тип**: `float`

### `OperationsHistoryItem`

::: steam_trader.OperationsHistoryItem
> Класс, представляющий информацию о предмете в истории операций.

`id`
> ID Операции.
> 
> **Тип**: `int`

`name`
> Название операции.
> 
> **Тип**: `str`

`type`
> Тип операции. 0 - продажа, 1 - покупка.
> 
> **Тип**: `int`

`amount`
> Сумма операции.
> 
> **Тип**: `float`

`currency`
> Валюта, значение 1 - рубль.
> 
> **Тип**: `int`

`date`
> Timestamp операции.
> 
> **Тип**: `int`

### `AltWebSocketMessage`

::: steam_trader.AltWebSocketMessage
> Класс, представляющий AltWebSsocket сообщение.

`type`
> 
> **Тип**: `int`

`data`
>
> **Тип**: `str`
