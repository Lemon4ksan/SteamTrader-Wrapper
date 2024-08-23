import os
import unittest
import steam_trader
from typing import Sequence
from steam_trader.constants import SUPPORTED_APPIDS, TEAM_FORTRESS_APPID
from steam_trader.exceptions import WrongTradeLink, NoTradeItems, Unauthorized

from dotenv import load_dotenv

load_dotenv()  # Для проведения тестов необходимо указать ваш токен и ссылку для обмена Steam в environemntal variables


class IndependentTests(unittest.TestCase):

    def setUp(self):
        self.client = steam_trader.Client(os.getenv('TOKEN'))

    def test_get_item_info(self):
        test_response = {
            'success': True,
            'name': 'Карманный мурлыка',
            'hash_name': 'The Pocket Purrer',
            'type': 'Сумка 37-го уровня',
            'gameid': 440,
            'contextid': 2,
            'color': '7D6D00',
            'small_image': 'https://',
            'large_image': 'https://',
            'marketable': False,
            'tradable': True,
            'description': 'kitty in a pocket',
            'market_price': 9.00,
            'buy_price': None,
            'steam_price': None,
            'filters':
            {
                'quality': [(28, 'Уникальный', '7D6D00')],
                'type': [(45, 'Акссессуар', None)],
                'class': [(32, 'Инженер', None)],
                'craft': [(277, 'Можно перековывать', None)]
            },
            'sell_offers': [
                {
                    'id': 104,
                    'classid': 2,
                    'instanceid': 3,
                    'itemid': 4,
                    'price': 5,
                    'currency': 1
                }
            ],
            'buy_offers': [
                {
                    'id': 105,
                    'price': 200,
                    'currency': 1
                }
            ],
            'sell_history': [
                [1, 2],
                [3, 4],
                [5, 6]
            ]
        }
        item_info = steam_trader.ItemInfo.de_json(test_response, client=self.client)
        for name, value in test_response.items():
            self.assertEqual(value, item_info.__getattribute__(name))

if __name__ == '__main__':
    unittest.main()
