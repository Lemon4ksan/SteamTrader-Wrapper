# SteamTrader-Wrapper
![PyPI - Downloads](https://img.shields.io/pypi/dm/steam-trader)
![PyPI - License](https://img.shields.io/pypi/l/steam-trader)
![PyPI - Status](https://img.shields.io/pypi/status/steam-trader)

<p align="left">
	<a href="https://discord.gg/DGRHEnUW">
      <img height="35.48" alt="Сервер" src="https://github.com/user-attachments/assets/b7c8a272-b48c-411f-aca3-6512086a9a18">
   </a>
</p>

⚠️ Это неофициальная библиотека.

### Содержание
  - [Введение](#введение)
    - [Получение токена](#получение-токена)
  - [Установка](#установка)
  - [Начало работы](#начало-работы)
  - [Примеры](#примеры)
  - [Документация](#документация)
  - [Лицензия](#лицензия)


### Введение

Эта библиотека представляет Python обёртку для API [Steam-Trader](https://steam-trader.com/).

Она совместима с версиями Python 3.12+ и поддерживает работу как с синхронным, так и с асинхронным (asyncio) кодом.

В дополнение к реализации чистого API данная библиотека имеет ряд объектов высокого уровня и логирование, 
дабы сделать разработку клиентов и скриптов простой и понятной. Документация была написана исходя из API документации сайта.

#### Получение токена

Токен можно получить на сайте перейдя на вкладку [API](https://steam-trader.com/api/). В коде указывается один раз при создании клиента.

### Установка

Вы можете установить или обновить Steam-Trader API с помощью команды:

```shell
pip install steam-trader
```

Или можете построить билд на основе репозитория:

```shell
git clone https://github.com/Lemon4ksan/SteamTrader-Wrapper
cd SteamTrader-Wrapper
python setup.py install
```

### Начало работы

Приступив к работе, первым делом необходимо создать экземпляр клиента.

```python
from steam_trader import Client

client = Client('Ваш токен')

# или

from steam_trader import ClientAsync

client = ClientAsync('Ваш токен')
```

Для использования логирования, добавьте эти строчки в свой код. Будет приходить полученный результат всех методов, 
а если указать уровень logging.DEBUG, то будут приходить входы и выходы из функций.

```python
import logging

logging.basicConfig(level=logging.INFO)
```

Все результаты запросов на сервер представлены в виде датаклассов, вы можете легко получить их данные используя аттрибуты.

```python
operations_history = client.get_operations_history()
for operation in operations_history.data:
    print(operation.type, operation.date)
```

Тайп хинты также указаны, это поможет вашему IDE определять неправильные операции с данными.

Библиотека предусматривает множество возможных ошибок, чтобы вы могли контролировать поведение программы при их возникновении.
Присутствуют константы для игр, которые поддерживает сайт.

```python
from steam_trader.exceptions import Unauthorized, UnknownItem, WrongTradeLink
from steam_trader.constants import TEAM_FORTRESS2_APPID, TF2_CRAFTABLE, DOTA2_RARITY_COMMON
```

### Примеры

Пример скрипта для продажи всего Очищенного металла в инвентаре TF2 с помощью синхронного клиента.

```python
from steam_trader import Client
from steam_trader.constants import TEAM_FORTRESS2_APPID

client = Client('Ваш токен')

inventory = client.get_inventory(TEAM_FORTRESS2_APPID)
new_price = client.get_min_prices(1226).market_price - 0.01
for item in inventory.items:
    if item.gid == 1226:
        client.sell(item.itemid, item.assetid, price=new_price)
```

С помощью get_inventory мы получаем все предметы из инвенторя TF2, которые не находятся в продаже, проходим по каждому, 
находим Очищенный металл и выставляем его по цене на копейку меньше рыночной, чтобы быть впереди. Узнать минимальную стоимость предмета можно через get_min_prices.

Пример покупки всех предметов по GID ниже заданной стоимости.

```python
from steam_trader import Client
from steam_trader.exceptions import NotEnoughMoney

client = Client('Ваш токен')

max_price = 9.00
gid = 3242

sell_offers = client.get_order_book(gid, mode='sell')
for offer in sell_offers.sell:
    if offer[0] < max_price:
        for _ in range(offer[1]):
            try:
                client.buy(gid, 1, offer[0])
            except NotEnoughMoney:
                exit('Не хватает денег :(')
```

С помощью get_order_book мы получаем все предложения о продаже, проходимся по каждому, если цена предложения меньше нашей максимальной, то мы покупаем все предложения по данной цене.
Также мы используем исключение, если нам не хватит денег на покупку в любой момент.

Последним примером будет использование асинхронного клиента для получения запросов информации большого числа предметов.

```python
import asyncio
from steam_trader import ClientAsync

client = ClientAsync('Ваш токен')

gids = [1226, 1402, 3439, 1976, 1984, 1990, 1227, 1205, 1523, 2484, 1524, 1503, 1506, 1220, 1515, 3530, 1745, 1202]

async def main():
    async with client:
        tasks = [client.get_item_info(gid) for gid in gids]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

asyncio.run(main())
```

Благодаря асинхронности, мы отправили все запросы на сервер *одновременно* и получили результат намного быстрее, чем с синхронным клиентом.
Мы не ждём ответа при каждом запросе, а переключаемся на другой. Если вам это не понятно, изучите модуль asyncio.

### Документация

Полную документацию можно найти здесь: https://lemon4ksan.github.io/steam-trader/

### Внесение своего вклада в проект 

Внесение своего вклада максимально приветствуется!

Вы можете помочь, сообщив о [баге](https://github.com/Lemon4ksan/SteamTrader-Wrapper/issues/new?assignees=&labels=bug&projects=&template=bug-report.md&title=) или [предложив](https://github.com/Lemon4ksan/SteamTrader-Wrapper/issues/new?assignees=&labels=feature-request&projects=&template=feature-request.md&title=) новый функционал.

Данная библиотека будет переодически обновляться и дополняться.

### Лицензия
См. Оригинал на английском [LICENSE](https://github.com/Lemon4ksan/SteamTrader-Wrapper/blob/master/LICENSE)

Разрешается повторное распространение и использование как в виде исходного кода, так и в двоичной форме, с изменениями или без, при соблюдении следующих условий:

- При повторном распространении исходного кода должно оставаться указанное выше уведомление об авторском праве, этот список условий и последующий отказ от гарантий.
- При повторном распространении двоичного кода должна сохраняться указанная выше информация об авторском праве, этот список условий и последующий отказ от гарантий в документации и/или в других материалах, поставляемых при распространении.
- Ни имя автора, ни имена участников не могут быть использованы в качестве поддержки или продвижения продуктов, основанных на этом ПО без предварительного письменного разрешения.

ЭТА ПРОГРАММА ПРЕДОСТАВЛЕНА ВЛАДЕЛЬЦАМИ АВТОРСКИХ ПРАВ И/ИЛИ ДРУГИМИ СТОРОНАМИ «КАК ОНА ЕСТЬ» БЕЗ КАКОГО-ЛИБО ВИДА ГАРАНТИЙ, ВЫРАЖЕННЫХ ЯВНО ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ, ПОДРАЗУМЕВАЕМЫЕ ГАРАНТИИ КОММЕРЧЕСКОЙ ЦЕННОСТИ И ПРИГОДНОСТИ ДЛЯ КОНКРЕТНОЙ ЦЕЛИ. НИ В КОЕМ СЛУЧАЕ НИ ОДИН ВЛАДЕЛЕЦ АВТОРСКИХ ПРАВ И НИ ОДНО ДРУГОЕ ЛИЦО, КОТОРОЕ МОЖЕТ ИЗМЕНЯТЬ И/ИЛИ ПОВТОРНО РАСПРОСТРАНЯТЬ ПРОГРАММУ, КАК БЫЛО СКАЗАНО ВЫШЕ, НЕ НЕСЁТ ОТВЕТСТВЕННОСТИ, ВКЛЮЧАЯ ЛЮБЫЕ ОБЩИЕ, СЛУЧАЙНЫЕ, СПЕЦИАЛЬНЫЕ ИЛИ ПОСЛЕДОВАВШИЕ УБЫТКИ, ВСЛЕДСТВИЕ ИСПОЛЬЗОВАНИЯ ИЛИ НЕВОЗМОЖНОСТИ ИСПОЛЬЗОВАНИЯ ПРОГРАММЫ (ВКЛЮЧАЯ, НО НЕ ОГРАНИЧИВАЯСЬ ПОТЕРЕЙ ДАННЫХ, ИЛИ ДАННЫМИ, СТАВШИМИ НЕПРАВИЛЬНЫМИ, ИЛИ ПОТЕРЯМИ, ПРИНЕСЕННЫМИ ИЗ-ЗА ВАС ИЛИ ТРЕТЬИХ ЛИЦ, ИЛИ ОТКАЗОМ ПРОГРАММЫ РАБОТАТЬ СОВМЕСТНО С ДРУГИМИ ПРОГРАММАМИ), ДАЖЕ ЕСЛИ ТАКОЙ ВЛАДЕЛЕЦ ИЛИ ДРУГОЕ ЛИЦО БЫЛИ ИЗВЕЩЕНЫ О ВОЗМОЖНОСТИ ТАКИХ УБЫТКОВ.
