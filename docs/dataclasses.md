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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* MultiBuyOrder, optional ], optional

`left`
> Сколько предметов по этой цене осталось. Если операция прошла успешно, всегда равен 0.
> 
> **Тип**: `int`

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* `ItemForExchange`, optional ]

`description`
> Описания предметов для обмена с ботом. Ключ - itemid предмета.
> 
> **Тип**: dict[ int, *class* `TradeDescription` ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

### `ExchangeResult`

::: steam_trader.ExchangeResult
> Класс, представляющий результат обмена с ботом.

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
> **Тип**: `int`

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
> **Тип**: Sequence[ *class* `ExchangeItem`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

### `ExchangeP2PResult`

`success`
> Результат запроса.
> 
> **Тип**: `bool`

`send`
> Массив с данными для создания нового обмена в Steam.
> 
> **Тип**: Sequence[ *class* `P2PSendObject`, optional ]

`recieve`
> Массив с данными для принятия обмена.
> 
> **Тип**: Sequence[ *class* `RecieveObject`, optional ]

`confirm`
> Массив с данными для подтверждения обмена в мобильном аутентификаторе.
> 
> **Тип**: Sequence[ *class* `ConfirmObject`, optional ]

`cancel`
> Массив из ID обменов, которые нужно отменить.
> 
> **Тип**: Sequence[ `str` ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* `SellOffer`, optional ]

`buy_offers`
> Последовательность с предложениями о покупке.
> 
> **Тип**: Sequence[ *class* `BuyOffer`, optional ]

`sell_history`
> Последовательность истории продаж.
> 
> **Тип**: Sequence[ *class* `SellHistoryItem`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* `InventoryItem`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* `BuyOrder`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: dict[ `int`, *class* `BuyOrder`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* `OperationsHistoryItem`, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

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
> **Тип**: Sequence[ *class* AltWebSocketMessage, optional ]

`client`
> Клиент Steam Trader.
> 
> **Тип**: Union[ *class* `Client`, *class* `ClientAsync`, `None` ]

