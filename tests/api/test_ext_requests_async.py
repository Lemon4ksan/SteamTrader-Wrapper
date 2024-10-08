"""
Эти тесты проверяют отправку get и post запросов на сервер.
Тесты, которые могут повлиять на состояние вашего инвентаря по умолчанию пропускаются
"""

import os
import unittest

from steam_trader.api import Filters, Filter
from steam_trader.api.ext import ExtClientAsync
from steam_trader.constants import *

from dotenv import load_dotenv
load_dotenv()  # Для проведения тестов необходимо указать ваш токен и ссылку для обмена Steam в environemntal variables

class IndependentTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = ExtClientAsync(os.getenv('TOKEN'))
        self.filters = Filters(
            quality=[Filter(id=TF2_QUALITY_STRANGE), Filter(id=DOTA2_QUALITY_ELDER)],
            type=[Filter(id=TF2_TYPE_PRIMARY), Filter(id=DOTA2_TYPE_STICKER)],
            used_by=[Filter(id=TF2_CLASS_ENGINEER), Filter(id=TF2_CLASS_SCOUT)]
        )
        self.SKIP_SELL_TESTS = True
        self.TEST_GID = 1828

    async def test_get_inventory(self):
        async with self.client:
            inventory = await self.client.get_inventory(TEAM_FORTRESS2_APPID, status=[0, 1, 2, 3, 4])
            self.assertTrue(inventory.success)

    async def test_get_inventory_with_filters(self):
        async with self.client:
            inventory = await self.client.get_inventory(TEAM_FORTRESS2_APPID, filters=self.filters, status=[0, 1, 2, 3, 4])
            self.assertTrue(inventory.success)

    async def test_multi_sell(self):
        async with self.client:
            if self.SKIP_SELL_TESTS:
                self.skipTest('Тест на мульти-продажу пропущен.')

            multi_sell_result = await self.client.multi_sell(440, 1226, 2.92, 1)
            self.assertTrue(multi_sell_result[0].success)

    async def test_set_trade_mode(self):
        async with self.client:
            result = await self.client.set_trade_mode(0)
            self.assertTrue(result.success)
            result = await self.client.set_trade_mode(1)
            self.assertTrue(result.success)

    async def test_get_price_range(self):
        async with self.client:
            price_range = await self.client.get_price_range(self.TEST_GID)
            self.assertIsInstance(price_range.lowest, float)
            self.assertIsInstance(price_range.highest, float)

if __name__ == '__main__':
    unittest.main()
