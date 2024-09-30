"""Данный скрипт автоматически изменяет цену предметов так, чтобы быть первым в очереди и выводит красивую статистику.
В данном примере будут использованы все предметы TF2 на продаже. Можете свободно использовать код в своих целях.
"""

from time import sleep
from datetime import datetime
from steam_trader.api import Client

client = Client('Ваш токен')

with client:
    while True:
        sell_items = client.get_inventory(440, status=[0]).items
        for item in sell_items:

            if item.price == 0.5:
                continue

            market_price = client.get_min_prices(item.gid).market_price
            sell_orders = client.get_order_book(item.gid)

            new_price = round(market_price - 0.01, 2)
            if item.price > market_price and new_price > sell_orders.buy[0][0]:
                print(f'{datetime.now():%H:%M:%S} | '
                      f'{client.get_item_info(item.gid).name.center(67)} | '
                      f'{str(item.price).center(8)} -> {str(new_price).center(8)} | '
                      f'уменьшение')

                client.edit_price(item.id, new_price)

            elif item.price < round(sell_orders.sell[1][0] - 0.01, 2) and sell_orders.sell[0][1] == 1:
                new_price = round(sell_orders.sell[1][0] - 0.01, 2)
                print(f'{datetime.now():%H:%M:%S} | '
                      f'{client.get_item_info(item.gid).name.center(67)} | '
                      f'{str(item.price).center(8)} -> {str(new_price).center(8)} | '
                      f'увеличение')

                client.edit_price(item.id, new_price)

        sleep(30)
