# Асинхронный клиент

Асинхронный клиент позволяет создавать обльшое количество запросов более эффективно. Он не всегда неоюходим, но часто незаменим.
Этот раздел пройдётся по тому, как его настроить.

## Инициализация клиента
Инициализация асинхронного клиента похожа на инициализацию синхронного.

```python
from steam_trader import ClientAsync

client = steam_trader.ClientAsync('Ваш токен')
```

Для того чтобы создавать асинхронные запросы, необходимо поместить ваш код в асинхронную функцию.
```python
from steam_trader import ClientAsync

client = steam_trader.ClientAsync('Ваш токен')

async def main()
    ...
```

Для работы с клиентом нужно использовать асинхронный контекстный менеджер.
```python
from steam_trader import ClientAsync

client = steam_trader.ClientAsync('Ваш токен')

async def main()
    async with client:
        ...
```

При вызове асинхронной функции она не выполняется, а возвращает объект корутины.
С помощью await мы показываем где мы будем ждать чего-то.
```python
from steam_trader import ClientAsync

client = steam_trader.ClientAsync('Ваш токен')

async def main()
    async with client:
        operations_history = await client.get_operations_history()
```

Если вы попробуете вызвать функцию main, то получите ошибку. Асинхронные функции нужно вызывать с помощью встроенного модуля asyncio.

```python
import asyncio
from steam_trader import ClientAsync

client = steam_trader.ClientAsync('Ваш токен')

async def main()
    async with client:
        operations_history = await client.get_operations_history()

if __name__ == '__main__':
    asyncio.run(main())
```

Теперь клиент готов к выполнению задач.

## Пример использования
Представим, что нам нужно получить информацию о большом количестве предметов.
Для начала напишем код для синхронного клиента.

```python
from steam_trader import ClientAsync

client = ClientAsync('Ваш токен')

gids = [1226, 1402, 3439, 1976, 1984, 1990, 1227, 1205, 1523, 2484, 1524, 1503, 1506, 1220, 1515, 3530, 1745, 1202]

def main():
    with client:
        for gid in gids:
            client.get_item_info(gid)

if __name__ == '__main__':
    main()
```

Замерим скорость выполнения.
```pycon
>>> from timeit import timeit
>>> timeit(main, number=1)
# 3.7272357000038028
```
Данный запрос занял 3 секунды, может показаться, что это немного, но что будет если таких запросов будет 5 а не 1?

В оптимизации нам поможет асинхронный клиент.

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

Замерим скорость выполнения.
```pycon
>>> from timeit import timeit
>>> timeit(main, number=1)
# 1.1095618000254035
```
Как мы выдим, результат пришёл в 3 раза быстрее! Но как это работает?
Сначала мы создаём все корутины, которые мы собираемся выполнить, затем с помощью asyncio.gather() мы выполняем их *одновременно*.
Благодаря асинхронности, интерпретатор не ждёт пока с сервера придёт один запрос, а переключается на следующий.

Это далеко не единственный пример использования асинхронного клиента, но определённо самый простой для понимания.