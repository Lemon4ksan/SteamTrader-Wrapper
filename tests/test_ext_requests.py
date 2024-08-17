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

    def test_get_inventory(self):
        inventory = self.client.get_inventory(TEAM_FORTRESS_APPID)
        self.assertTrue(inventory.success)

    def test_get_inventory_with_filters(self):
        inventory = self.client.get_inventory(TEAM_FORTRESS_APPID, filters=self.filters)
        self.assertTrue(inventory.success)

if __name__ == '__main__':
    unittest.main()
