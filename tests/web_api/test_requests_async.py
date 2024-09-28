import os
import unittest
from dotenv import load_dotenv
import steam_trader.web as steam_trader
from steam_trader.constants import SUPPORTED_APPIDS
from steam_trader.exceptions import *
load_dotenv()  # Для проведения тестов необходимо указать sessionid (sid) в environemntal variables

class IndependentTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.client = steam_trader.WebClientAsync(os.getenv('SESSIONID'))
        self.test_gids = [1220, 1226, 1760, 6231, 6339, 13903, 14324, 71603]
        self.test_appids = SUPPORTED_APPIDS

    async def test_get_main_page(self):
        async with self.client:
            for appid in self.test_appids:
                result = await self.client.get_main_page(appid, items_on_page=30)
                self.assertTrue(result.auth)
                self.assertTrue(len(result.items) == 30)

            with self.assertRaises(NotFoundError):
                await self.client.get_main_page(appid, text='__UNDEFINED__')

    async def test_get_item_info(self):
        async with self.client:
            for gid in self.test_gids:
                result = await self.client.get_item_info(gid, items_on_page=30)
                self.assertTrue(result.auth)

    async def test_get_referral_link(self):
        async with self.client:
            result = await self.client.get_referral_link()
            self.assertIsInstance(result, str)

    async def test_get_referrals(self):
        async with self.client:
            result = await self.client.get_referrals()
            self.assertIsInstance(result, list)

    async def test_get_history(self):
        async with self.client:
            await self.client.get_history_page(440, 'last_purchases')
            await self.client.get_history_page(440, 'day_most')
            await self.client.get_history_page(440, 'all_time_most')

if __name__ == '__main__':
    unittest.main()
