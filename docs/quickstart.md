# Начало работы

## Получение ключа
Перед началом работы необходимо получить токен для авторизации. Его можно получить [тут](https://steam-trader.com/api/).

## Инициализация клиента
Начнём с импортирования библиотеки
```python
import steam_trader
```

Есть несколько способов работать с запросами: синхронно и асинхронно. Здесь мы разберём работу с синхронным клиентом.
```python
from steam_trader import Client

client = steam_trader.Client('Ваш токен')
```

Для оптимизации общения между клиентом и сервером можно также использовать контекстный менеджер with для поддержания сеанса, но это необязательно.
```python
from steam_trader import Client

client = steam_trader.Client('Ваш токен')
with client:
    # Ваш код здесь
```

## Основные понятия в запросах
Далее в документации будут упоминаться определённые термины, которые необходимо понимать.

### Что такое AppID, AssetID, ClassID, InstanceID и ContextID?

AppID - это идентификатор игры с которой вы хотите взаимодействовать, или относится предмет.

AppID можно встретить в большинстве операций с предметами. Рекомендуется использовать константы для большего понимания.
```python
from steam_trader.constants import TEAM_FORTRESS2_APPID, DOTA2_APPID
from steam_trader.constants import SUPPORTED_APPIDS
```
---
AssetID - это уникальный идентификатор для актива (предмета) в Steam. Активы также имеют ClassID и InstanceID, которые являются указанием на фактическое представление элемента.
Объекты активов также могут иметь свойства количества, чтобы указать, сколько этого точного экземпляра пользователь имеет в случае однотипных предметов.
Идентификаторы активов также могут меняться при торговле предметом, хотя classid и instanceid должны оставаться прежними, ЕСЛИ свойства предмета не изменились во время торговли.

AssetID можно встретить в get_items_for_exchange(), get_items_for_exchange_p2p(), exchange(), exchange_p2p() и get_inventory().

---
ClassID - это идентификатор, который определяет класс элемента, свойства которого одинаковы для всех элементов с этим идентификатором класса.

ClassID можно встретить в get_items_for_exchange(), get_items_for_exchange_p2p(), exchange(), exchange_p2p() и get_item_info().

---
InstanceID - Это идентификатор, описывающий экземпляр элемента, который наследует свойства от класса, причём идентификатор класса указан в экземпляре.

InstanceID можно встретить в get_items_for_exchange(), get_items_for_exchange_p2p(), exchange(), exchange_p2p() и get_item_info().

---
ContextID - это способ организации/категоризирования предметов/активов/валюты. 
Это просто целое число, но в документации Steam описывается способ сделать его в некоторой степени основанным на папках,
разделив целое число на диапазоны битов и используя каждый диапазон битов для обозначения чего-то другого.

ContextID можно встретить в get_items_for_exchange(), get_items_for_exchange_p2p(), exchange(), exchange_p2p() и get_item_info().

### Что такое GID и ItemID?

GID - Это идентификатор группы предметов. Под ним подразумеваются все предложения о продаже предмета и общая информация о нём.

GID можно найти в ссылке при просмотре на сайте или в предметах, получаемых через get_inventory() или напрямую через сайт.
```
https://steam-trader.com/tf2/1226-Refined-Metal
                   |---------^^^^----------|
                   Данные цифры являются GID
```
Если вы хотите самостоятельно посмотреть предмет с соответствующим GID, вы можете поменять эти цифры на другие.

---
ItemID - Это идентификатор конкретного предмета. Он позволяет отличить его от других предметов в одной категории.
ItemID можно получить при покупке предмета или через get_inventory().


## Создание запросов
Для создания запросов необходимо использовать предоставленные клиентом методы. Весь их список можно найти в [Справочнике по API](client.md).

```python
from steam_trader import Client
from steam_trader.constants import TEAM_FORTRESS2_APPID

client = steam_trader.Client('Ваш токен')

item_info = client.get_item_info(1220)
inventory = client.get_inventory(TEAM_FORTRESS2_APPID, status=[0, 1, 2])
```

После выполнения запроса возвращается объект класса с ответом от сервера. Чтобы получить значения, используйте соответствующие аттрибуты.

```python
from steam_trader import Client

client = steam_trader.Client('Ваш токен')

orders = client.get_order_book(1556)
sell_orders = orders.sell
buy_orders = orders.buy

inventory_items = client.get_inventory(440, status=[0]).items  # Предметы на продаже
for inventory_item in inventory_items:
    print(inventory_item.name, inventory_item.price)
```

## Работа с исключениями
Во время выполнения вашей программы могут прийти неудачные ответы от сервера. Вам необходимо предусмотреть действия при их возникновении.
Данная библиотека предоставляет все ошибки, которые могут произойти на сайте.

```python
from steam_trader import Client
from steam_trader import exceptions

client = steam_trader.Client('Ваш токен')

try:
    client.buy(40814)
except exceptions.NotEnoughMoney:
    print('Не хватает денег для покупки.')
except exceptions.NoTradeLink:
    print('Не указана ссылка для обмена')
except exceptions.SteamTraderError as e:
    print(f'Произошла непредусмотренная ошибка: {e}')
```

## Использование констант
Для того чтобы вам не пришлось запоминать все уникальные ID, в библиотеке предусмотренны константы.

```python
from steam_trader.constants import TEAM_FORTRESS2_APPID, DOTA2_APPID
from steam_trader.constants import SUPPORTED_APPIDS

# или

from steam_trader import constants
print(constants.TF2_TYPE_PRIMARY)
```

## Подключение логов
Согласитесь, писать принты каждый раз для проверки валидности данных утомляет. Поэтому данная библиотека поддерживает логи!
Чтобы подключить логирование, добавьте следующие строчки в свой код:

```python
import logging

logging.basicConfig(level=logging.INFO)
```

!!! Подсказка
    Если вы не хотите получать логи от модуля httpx то добавите это в свой код: ```logging.getLogger('httpx').setLevel(logging.WARNING)```.
    Так вы будете получать только логи предупреждения и выше.

## Заключение
Теперь вы знаете всё для начала работы. Для дальнейшего ознакомления изучите работу с [асинхронным клиентом](async.md) и [ext функционалом](ext_guide.md).

Для полного содержания библиотеки см. [Справочник по API](client.md)

Также можете иузчить готовые [примеры скриптов](https://github.com/Lemon4ksan/SteamTrader-Wrapper/tree/master/examples).
