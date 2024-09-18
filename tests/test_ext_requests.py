"""
Эти тесты проверяют отправку get и post запросов на сервер.
Тесты, которые могут повлиять на состояние вашего инвентаря по умолчанию пропускаются
"""

import os
import unittest

from steam_trader import Filters, Filter
from steam_trader.ext import ExtClient
from steam_trader.constants import *

from dotenv import load_dotenv
load_dotenv()  # Для проведения тестов необходимо указать ваш токен и ссылку для обмена Steam в environemntal variables

class IndependentTests(unittest.TestCase):

    def setUp(self):
        self.client = ExtClient(os.getenv('TOKEN'))
        self.filters = Filters(
            quality=[Filter(id=TF2_QUALITY_STRANGE), Filter(id=DOTA2_QUALITY_ELDER)],
            type=[Filter(id=TF2_TYPE_PRIMARY), Filter(id=DOTA2_TYPE_STICKER)],
            used_by=[Filter(id=TF2_CLASS_ENGINEER), Filter(id=TF2_CLASS_SCOUT)]
        )
        self.SKIP_SELL_TESTS = True
        self.TEST_GID = 1828

    def test_get_inventory(self):
        inventory = self.client.get_inventory(TEAM_FORTRESS2_APPID, status=[0, 1, 2, 3, 4])
        self.assertTrue(inventory.success)

    def test_get_inventory_with_filters(self):
        inventory = self.client.get_inventory(TEAM_FORTRESS2_APPID, filters=self.filters, status=[0, 1, 2, 3, 4])
        self.assertTrue(inventory.success)

    def test_multi_sell(self):
        if self.SKIP_SELL_TESTS:
            self.skipTest('Тест на мульти-продажу пропущен.')

        multi_sell_result = self.client.multi_sell(440, 1226, 2.92, 1)
        self.assertTrue(multi_sell_result[0].success)

    def test_set_trade_mode(self):
        result = self.client.set_trade_mode(0)
        self.assertTrue(result.success)
        result = self.client.set_trade_mode(1)
        self.assertTrue(result.success)

    def test_get_price_range(self):
        price_range = self.client.get_price_range(self.TEST_GID)
        self.assertIsInstance(price_range.lowest, float)
        self.assertIsInstance(price_range.highest, float)

if __name__ == '__main__':
    unittest.main()
