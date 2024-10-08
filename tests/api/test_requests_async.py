"""
Эти тесты проверяют отправку асинхронных get и post запросов на сервер.
Тесты, которые могут повлиять на состояние вашего инвентаря по умолчанию пропускаются
"""

import os
import unittest
import asyncio
import steam_trader.api as steam_trader
from collections.abc import Sequence
from steam_trader.constants import SUPPORTED_APPIDS, TEAM_FORTRESS2_APPID
from steam_trader.exceptions import WrongTradeLink, NoTradeItems

from dotenv import load_dotenv
load_dotenv()  # Для проведения тестов необходимо указать ваш токен и ссылку для обмена Steam в environemntal variables

class IndependentTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.ClientAsync(os.getenv('TOKEN'))
        self.test_gids = [1220, 1226, 1760, 6231, 6339, 13903, 14324, 71603]
        self.test_appids = SUPPORTED_APPIDS

    async def test_balance(self):
        async with self.client:
            balance = await self.client.balance
            self.assertIsInstance(balance, float)

    async def test_get_min_prices(self):
        async with self.client:
            tasks = [self.client.get_min_prices(gid) for gid in self.test_gids]
            responses = await asyncio.gather(*tasks)
            for min_prices in responses:
                self.assertTrue(min_prices.success)

    async def test_get_item_info(self):
        async with self.client:
            tasks = [self.client.get_item_info(gid) for gid in self.test_gids]
            responses = await asyncio.gather(*tasks)
            for item_info in responses:
                self.assertTrue(item_info.success)

    async def test_get_order_book(self):
        async with self.client:
            tasks = [self.client.get_order_book(gid) for gid in self.test_gids]
            responses = await asyncio.gather(*tasks)
            for order_book in responses:
                self.assertTrue(order_book.success)

    async def test_get_web_socket_token(self):
        async with self.client:
            token = await self.client.get_web_socket_token()
            self.assertIsInstance(token, steam_trader.WebSocketToken)

    async def test_get_inventory(self):
        async with self.client:
            tasks = [self.client.get_inventory(appid, status=[0, 1, 2, 3, 4]) for appid in self.test_appids]
            responses = await asyncio.gather(*tasks)
            for inventory in responses:
                if not inventory.success:
                    self.assertIsInstance(inventory.items, Sequence)
                else:
                    self.assertTrue(inventory.success)

    async def test_get_discounts(self):
        async with self.client:
            discounts = await self.client.get_discounts()
            self.assertTrue(discounts.success)

    async def test_get_operations_history(self):
        async with self.client:
            operations_history = await self.client.get_operations_history()
            self.assertTrue(operations_history.success)

            tasks = [self.client.get_operations_history(operation_type=operation_type) for operation_type in range(1, 11)]
            responses = await asyncio.gather(*tasks)
            for operations_history in responses:
                self.assertTrue(operations_history.success)

    async def test_update_inentory(self):
        async with self.client:
            tasks = [self.client.update_inventory(appid) for appid in self.test_appids]
            await asyncio.gather(*tasks)

    async def test_get_inventory_state(self):
        async with self.client:
            tasks = [self.client.get_inventory_state(appid) for appid in self.test_appids]
            responses = await asyncio.gather(*tasks)
            for inventory_state in responses:
                self.assertTrue(inventory_state.success)

    async def test_trigger_alt_web_socket(self):
        async with self.client:
            result = await self.client.trigger_alt_web_socket()
            if isinstance(result, steam_trader.AltWebSocket):
                self.assertIsInstance(result.success, bool)

class TradeLinkTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.ClientAsync(os.getenv('TOKEN'))
        self.trade_link = os.getenv('STEAM_TRADE_LINK')

    async def test_01_remove_trade_link(self):
        async with self.client:
            await self.client.remove_trade_link()

    async def test_02_set_trade_link(self):
        async with self.client:
            try:
                await self.client.set_trade_link(self.trade_link)
            except WrongTradeLink:
                self.skipTest('Тест на изменение ссылки обмена пропущен (Ваша ссылку удалена).')

class BuyTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.ClientAsync(os.getenv('TOKEN'))
        self.skip_tests = True
        self.buy_gid = 1220  # Тренировочный ракетомёт
        self.multi_buy_gid = 1311  # Офицер запаса
        self.buy_order_gid = 1524  # Слонобой
        self.default_price = 0.5
        self.default_appid = TEAM_FORTRESS2_APPID

    async def test_01_buy(self):
        """Вы купите предмет по gid (по умолчанию - Тренировочный ракетомёт).
        Вы можете поменять его на тот, который необходимо (оставьте цену в 0.5). Другие способы покупки не проверяются т.к. требуют специфических условий.
        Данный тест пропускается по умолчанию."""

        if self.skip_tests:
            self.skipTest('Тест на покупку пропущен.')

        async with self.client:
            buy_result = await self.client.buy(self.buy_gid, 1, self.default_price)
            self.assertTrue(buy_result.success)

    async def test_02_multi_buy(self):
        """Вы купите предмет по gid (по умолчанию - Офицер запаса).
        Вы можете поменять его на тот, который необходимо (оставьте цену в 0.5).
        Данный тест пропускается по умолчанию."""

        if self.skip_tests:
            self.skipTest('Тест на мульти-покупку пропущен.')

        async with self.client:
            multi_buy_result = await self.client.multi_buy(self.multi_buy_gid, self.default_price, 1)
            self.assertTrue(multi_buy_result)

    async def test_03_create_buy_order(self):
        """Вы создадите запрос на покупку предмета по gid (по умолчанию - Слонобой)
        по цене price (по умолчанию - 0.5). Вы можете поменять его на тот, который необходимо.
        Данный тест пропускается по умолчанию."""

        if self.skip_tests:
            self.skipTest('Тест на запрос на покупку пропущен.')

        async with self.client:
            buy_order_result = await self.client.create_buy_order(self.buy_order_gid, self.default_price)
            self.assertTrue(buy_order_result.success)

    async def test_04_get_buy_orders(self):
        """Данный тест пропускается по умолчанию. См. test_create_buy_order"""

        if self.skip_tests:
            self.skipTest('Тест на получение запросов на покупку пропущен.')

        async with self.client:
            buy_orders = await self.client.get_buy_orders(gameid=self.default_appid, gid=self.buy_order_gid)
            self.assertTrue(buy_orders.success)

    async def test_05_get_down_orders(self):
        """Убирает все запросы на покупку, по умолчанию пропускается."""

        if self.skip_tests:
            self.skipTest('Тест на снятие запросов пропущен.')

        async with self.client:
            get_down_orders_result = await self.client.get_down_orders(self.default_appid, order_type='buy')
            self.assertTrue(get_down_orders_result.success)

class SellTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.ClientAsync(os.getenv('TOKEN'))
        self.skip_tests = True
        self.buy_gid = 1220  # Тренировочный ракетомёт
        self.multi_buy_gid = 1311  # Офицер запаса
        self.buy_order_gid = 1524  # Слонобой
        self.default_price = 0.5
        self.default_appid = TEAM_FORTRESS2_APPID

    async def test_01_sale(self):
        """Если self.SKIP_BUY_TEST = False вы создадите запрос на продажу первого предмета в вашем инвентаре TF2 по цене price (по умолчанию - 0.5).
         Можете изменить цену, чтобы он не продался автоматически. Данный тест пропускается по умолчанию."""

        if self.skip_tests:
            self.skipTest('Тест на продажу пропущен.')

        async with self.client:
            inventory = await self.client.get_inventory(self.default_appid)
            for item in inventory.items:
                if item.status == -2:
                    break

            item_on_sale = await self.client.sell(item.itemid, item.assetid, self.default_price)
            self.assertTrue(item_on_sale.success)
            self._id = item_on_sale.id

    async def test_02_edit_price(self):
        """Данный тест пропускается по умолчанию. См. test_sale"""

        if self.skip_tests:
            self.skipTest('Тест на изменение цены пропущен.')

        async with self.client:
            edit_price_result = await self.client.edit_price(self._id, 0.6)
            self.assertTrue(edit_price_result.success)

    async def test_03_delete_item(self):
        """Данный тест снимает заявку на продажу, по умолчанию пропускается."""

        if self.skip_tests:
            self.skipTest('Тест на снятия с продажи пропущен.')

        async with self.client:
            delete_item_result = await self.client.delete_item(self._id)
            self.assertTrue(delete_item_result.success)

class TradeTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.ClientAsync(os.getenv('TOKEN'))
        self.skip_tests = True

    async def test_01_get_items_for_exchange(self):

        if self.skip_tests:
            self.skipTest('Тест на получение предметов для обмена пропущен.')

        async with self.client:
            try:
                items_for_exchange = await self.client.get_items_for_exchange()
                self.assertTrue(items_for_exchange.success)
            except NoTradeItems:
                self.skipTest('Тест на получение предметов для обмена пропущен (нет предметов для обмена).')

    async def test_02_exchange(self):

        if self.skip_tests:
            self.skipTest('Тест на передачу предметов пропущен.')

        async with self.client:
            try:
                exchange_result = await self.client.exchange()
                self.assertTrue(exchange_result.success)
            except NoTradeItems:
                self.skipTest('Тест на передачу предметов пропущен (нет предметов для обмена).')

    async def test_03_get_items_for_exchange_p2p(self):

        if self.skip_tests:
            self.skipTest('Тест на получение предметов для p2p обмена пропущен.')

        async with self.client:
            try:
                items_for_exchange_p2p = await self.client.get_items_for_exchange_p2p()
                self.assertTrue(items_for_exchange_p2p.success)
            except NoTradeItems:
                self.skipTest('Тест на получение предметов для p2p обмена пропущен (нет предметов для обмена).')

    async def test_04_exchange_p2p(self):

        if self.skip_tests:
            self.skipTest('Тест на p2p передачу предметов пропущен.')

        async with self.client:
            try:
                exchange_result = await self.client.exchange_p2p()
                self.assertTrue(exchange_result.success)
            except NoTradeItems:
                self.skipTest('Тест на p2p передачу предметов пропущен (нет предметов для обмена).')


if __name__ == '__main__':
    unittest.main()
