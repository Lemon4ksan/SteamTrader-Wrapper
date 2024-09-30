import os
import unittest
import steam_trader.web as steam_trader
from steam_trader.constants import SUPPORTED_APPIDS
from steam_trader.exceptions import *
from dotenv import load_dotenv
load_dotenv()  # Для проведения тестов необходимо указать sessionid (sid) в environemntal variables

class IndependentTests(unittest.TestCase):

    def setUp(self):
        self.client = steam_trader.WebClient(os.getenv('SESSIONID'))
        self.test_gids = [1220, 1226, 1760, 6231, 6339, 13903, 14324, 71603]
        self.test_appids = SUPPORTED_APPIDS

    def test_get_main_page(self):
        for appid in self.test_appids:
            result = self.client.get_main_page(appid, items_on_page=30)
            self.assertTrue(result.auth)
            self.assertTrue(len(result.items) == 30)

        with self.assertRaises(NotFoundError):
            self.client.get_main_page(appid, text='__UNDEFINED__')

    def test_get_item_info(self):
        for gid in self.test_gids:
            result = self.client.get_item_info(gid, items_on_page=30)
            self.assertTrue(result.auth)

    def test_get_referral_link(self):
        result = self.client.get_referral_link()
        self.assertIsInstance(result, str)

    def test_get_referrals(self):
        result = self.client.get_referals()
        self.assertIsInstance(result, list)

    def test_get_history(self):
        self.client.get_history_page(440, 'last_purchases')
        self.client.get_history_page(440, 'day_most')
        self.client.get_history_page(440, 'all_time_most')

if __name__ == '__main__':
    unittest.main()
