"""Собирает данные всех предметов игры на сайте и преобразует их в csv файл. Данный процесс довольно длительный.
Можете свободно использовать код в своих целях (не спамьте сайт!)."""

import os
import csv
import asyncio
import logging
import steam_trader.constants as constants
import steam_trader.web as web
import steam_trader.api as api
from time import sleep
from dotenv import load_dotenv
from typing import Sequence


logging.basicConfig(level=logging.INFO)
load_dotenv()

client = web.WebClientAsync(timeout=None)
api_client = api.ClientAsync(os.getenv('TOKEN'), timeout=None)


async def get_pages(gid: int) -> Sequence[Sequence['web.MainPageItem']]:
    async with client:
        page_count = (await client.get_main_page(gid, items_on_page=60)).page_count
        tasks = [client.get_main_page(gid, items_on_page=60, page=i) for i in range(1, page_count + 1)]
        main_pages: Sequence['web.MainPage'] = await asyncio.gather(*tasks)

        pages = []
        for page in main_pages:
            pages.append(page.items)

        return pages


async def get_info(pages: Sequence[Sequence['web.MainPageItem']]) -> Sequence['api.ItemInfo']:
    info = []
    for page in pages:
        async with api_client:
            tasks = [api_client.get_item_info(item.gid) for item in page]
            info.extend(await asyncio.gather(*tasks))
        sleep(5)  # Увеличьте если возникают проблемы.

    return info


async def main(gid):

    pages = await get_pages(gid)
    items_info = await get_info(pages)

    items = []
    for item in pages:
        items.extend(item)  # Объединяем всё в один список

    with open('items.csv', 'w', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
        csvwriter.writerow(
            ['Название',
             'hash_name',
             'GID',
             'Кол-во предметов',
             'Цена',
             'Выгода',
             'Цена автопокупки',
             'Кол-во предложений покупки']
        )

        for item, info in zip(items, items_info):
            item: web.MainPageItem
            info: api.ItemInfo

            if info.steam_price is not None and info.market_price is not None:
                benefit = round(info.steam_price - info.market_price, 2)
            else:
                benefit = 0
            buy_price = info.buy_price

            csvwriter.writerow(
                [item.name,
                 item.hash_name,
                 item.gid,
                 item.count,
                 str(info.market_price).replace('.', ','),
                 str(benefit).replace('.', ','),
                 str(buy_price).replace('.', ',') if buy_price is not None else 0,
                 len(info.buy_offers)]
            )

    print(f'Было обработанно {len(items)} предметов')


if __name__ == '__main__':
    asyncio.run(main(constants.TEAM_FORTRESS2_APPID))
