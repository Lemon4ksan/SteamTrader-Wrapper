import os
import unittest
import steam_trader


class IndependentTests(unittest.TestCase):

    def setUp(self):
        self.client = steam_trader.Client(os.getenv('TOKEN'))

    def assertion(self, test_response, result):
        for name, value in test_response.items():
            self.assertEqual(value, result.__getattribute__(name))

    def test_sell_result(self):
        test_response1 = {
            "success": True,
            "id": 143865972,
            "position": 10,
            "fast_execute": False,
            "nc": "L8RJI7XX9qAtpnls"
        }
        test_response2 = {
            "success": True,
            "id": 143865972,
            "position": 0,
            "fast_execute": True,
            "price": 10.24,
            "commission": 1.5,
            "nc": "L8RJI7XX9qAtpnls"
        }
        result = steam_trader.SellResult.de_json(test_response1, client=self.client)
        self.assertion(test_response1, result)
        result = steam_trader.SellResult.de_json(test_response2, client=self.client)
        self.assertion(test_response2, result)

    def test_buy_result(self):
        test_response = {
            "success": True,
            "id": 123,
            "gid": 111,
            "itemid": 222,
            "price": 10.24,
            "new_price": 0,
            "discount": 1.5
        }
        result = steam_trader.BuyResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_create_buy_order_result(self):
        test_response = {
            "success": True,
            "orders": [
                {
                    "id": 10,
                    "position": 0,
                    "fast_execute": True,
                    "price": 10.24,
                    "discount": 1.5
                },
                {
                    "id": 11,
                    "position": 1,
                    "fast_execute": False
                },
                {
                    "id": 12,
                    "position": 2,
                    "fast_execute": False
                }
            ],
            "executed": 1,
            "placed": 2
        }
        result = steam_trader.BuyOrderResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_multi_buy_result(self):
        test_response = {
            "success": True,
            "balance": 10.53,
            "spent": 21,
            "orders": [
                {
                    "id": 1,
                    "itemid": 123,
                    "price": 10
                },
                {
                    "id": 2,
                    "itemid": 123,
                    "price": 11
                }
            ]
        }
        result = steam_trader.MultiBuyResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_edit_price_result(self):
        test_response1 = {
            "success": True,
            "type": 0,
            "position": 10,
            "fast_execute": False
        }
        test_response2 = {
            "success": True,
            "type": 0,
            "position": 0,
            "fast_execute": True,
            "new_id": 153726182,
            "price": 10.24,
            "percent": 1.5
        }
        result = steam_trader.EditPriceResult.de_json(test_response1, client=self.client)
        self.assertion(test_response1, result)
        result = steam_trader.EditPriceResult.de_json(test_response2, client=self.client)
        self.assertion(test_response2, result)

    def test_delete_item_result(self):
        test_response = {
            "success": True,
            "has_ex": True,
            "has_bot_ex": True,
            "has_p2p_ex": False,
            "total_fines": 0,
            "fine_date": None
        }
        result = steam_trader.DeleteItemResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_get_down_orders_result(self):
        test_response = {
            "success": True,
            "count": 3,
            "ids": [
                1,
                2,
                3
            ]
        }
        result = steam_trader.GetDownOrdersResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_items_for_exchange(self):
        test_response = {
            "success": True,
            "items": [
                {
                    "id": 1222410,
                    "assetid": "1354689315",
                    "gameid": 730,
                    "contextid": 2,
                    "classid": "469445126",
                    "instanceid": "302028390",
                    "gid": 2435,
                    "itemid": 8656,
                    "price": 1,
                    "currency": 1,
                    "timer": 3600,
                    "asset_type": 1,
                    "percent": 1.5,
                    "steam_item": True
                }
            ],
            "descriptions": {
                "8656": {
                    "type": "Пулемёт, Ширпотреб",
                    "description": """Внешний вид: Немного поношенное
                        Пулемет Negev, благодаря вместительному магазину и высокой скорострельности,
                        идеально подходит для стрельбы залпом.
                        Его положительные качества омрачаются очень высокой ценой,
                        большим разбросом и раздражающей отдачей.
                        Покрыто металлической фольгой с оттиском в виде камуфляжа.
                        Помни то, чему научился
                        Коллекция «Bank»""",
                    "hash_name": "Negev | Army Sheen (Minimal Wear)",
                    "name": "Negev | Армейский блеск (Немного поношенное)",
                    "image_small": "efbf1363d51593066952ec6585306494",
                    "color": "D2D2D2",
                    "outline": "B0C3D9",
                    "gameid": 730
                }
            }
        }
        result = steam_trader.ItemsForExchange.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_exchange_result(self):
        test_response = {
            "success": True,
            "offerId": "123456678",
            "code": "ABCD",
            "botSteamId": "76561198000000000",
            "botNick": "Bot nick",
            "items": [
                {
                    "id": 123,
                    "assetid": "456",
                    "gameid": 440,
                    "contextid": 2,
                    "classid": "111",
                    "instanceid": "222",
                    "type": 0,
                    "itemid": 1,
                    "gid": 1,
                    "price": 3.33,
                    "currency": 1,
                    "percent": 1.5
                }
            ]
        }
        result = steam_trader.ExchangeResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_exchange_p2p_result(self):
        test_response = {
            "success": True,
            "send": [
                {
                    "tradeLink": "https://steamcommunity.com/tradeoffer/new/?partner=899862691&token=NtCkMiJ5",
                    "tradeOffer":
                    {
                        "sessionid": "{sessionid}",
                        "serverid": 1,
                        "partner": "76561198860128419",
                        "tradeoffermessage": "2Q6B",
                        "json_tradeoffer": "{\"newversion\":true,\"version\":2,\"me\":{ \"assets\":[{\"appid\":730,\"contextid\":\"2\",\"amount\":1,\"assetid\":\"12345678910\"}], \"currency\":[],\"ready\":false},\"them\":{\"assets\":[],\"currency\":[],\"ready\":false}}",
                        "captcha": "",
                        "trade_offer_create_params": "{\"trade_offer_access_token\":\"NtCkMiJ5\"}",
                    }
                }
            ],
            "receive": [
                {
                    "offerId": "1234567890",
                    "code": "2Q6B",
                    "items": [
                        {
                            "id": 123,
                            "assetid": "12345678910",
                            "gameid": 730,
                            "contextid": 2,
                            "classid": "111",
                            "instanceid": "222",
                            "type": 1,
                            "itemid": 1,
                            "gid": 1,
                            "price": 3.33,
                            "currency": 1,
                            "percent": 1.5
                        }
                    ],
                    "partnerSteamId": "76561198860128419"
                }
            ],
            "confirm": [
                {
                    "offerId": "1234567890",
                    "code": "2Q6B",
                    "partnerSteamId": "76561198860128419"
                }
            ],
            "cancel": [
                "123",
                "456"
            ]
        }
        result = steam_trader.ExchangeP2PResult.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_min_prices(self):
        test_response = {
            "success": True,
            "market_price": 200,
            "buy_price": 200,
            "steam_price": 400,
            "count_sell_offers": 30,
            "count_buy_offers": 15
        }
        result = steam_trader.MinPrices.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_get_item_info(self):
        test_response = {
            "success": True,
            "name": "Арбалет крестоносца",
            "hash_name": "Crusader's Crossbow",
            "type": "Арбалет 15-го уровня",
            "gameid": 440,
            "contextid": 2,
            "color": "7D6D00",
            "small_image": "http://steam-trader.org/upload/items/130/72/72d9a85206e4a0f6df427041ea72a1ae.png",
            "large_image": "http://steam-trader.org/upload/items/400/72/72d9a85206e4a0f6df427041ea72a1ae.png",
            "marketable": False,
            "tradable": True,
            "description": """
            Без попаданий в голову.
            Боезапас основного оружия: -75 %
            Стреляет особыми снарядами, которые лечат союзников 
            и наносят урон в зависимости от дальности полета.
            Если убрать это оружие, оно перезарядится.
            Средневековый медик
            Ампутатор
            Арбалет крестоносца
            Боевой шлем берлинца""",
            "market_price": 100,
            "buy_price": 120,
            "steam_price": 200,
            "filters": {
                "quality": [
                    {
                        "id": 28,
                        "title": "Уникальный",
                        "color": "7D6D00"
                    }
                ],
                "type": [
                    {
                        "id": 45,
                        "title": "Основное оружие",
                        "color": None
                    }
                ],
                "class": [
                    {
                        "id": 34,
                        "title": "Медик",
                        "color": None
                    }
                ],
                "craft": [
                    {
                        "id": 277,
                        "title": "Можно перековывать",
                        "color": None
                    }
                ]
            },
            "sell_offers": [
                {
                    "id": 46,
                    "classid": "210",
                    "instanceid": "0",
                    "itemid": 46,
                    "price": 80,
                    "currency": 1
                },
                {
                    "id": 42,
                    "classid": "210",
                    "instanceid": "0",
                    "itemid": 46,
                    "price": 90,
                    "currency": 1
                }
            ],
            "buy_offers": [
                {
                    "id": 20,
                    "price": 80,
                    "currency": 1
                }
            ],
            "sell_history": [
                [1506137845, 20.00],
                [506137857, 401.00]
            ]
        }
        result = steam_trader.ItemInfo.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_order_book(self):
        test_response = {
            "success": True,
            "sell": [
                [1.15, 5],
                [1.94, 1],
                [2.72, 3]
            ],
            "buy": [
                [1, 1],
                [0.83, 2],
                [0.5, 5]
            ],
            "total_sell": 9,
            "total_buy": 8
        }
        result = steam_trader.OrderBook.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_ws_token(self):
        test_response = {
            "steam_id": "76561191234567890",
            "time": 1504281966,
            "hash": r"tQ+XqXYXVb+hX9M25wzj\/nhOR5LQyJATY1499qGdK2o="
        }
        result = steam_trader.WebSocketToken.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_inventory(self):
        test_response = {
            "success": True,
            "count": 1,
            "game": 440,
            "last_update": 1682937514,
            "items": [
                {
                    "id": 1222410,
                    "assetid": "3227691166",
                    "gid": 2435,
                    "itemid": 8656,
                    "price": 1,
                    "currency": 1,
                    "timer": 3600,
                    "type": 0,
                    "status": 1,
                    "position": None,
                    "nc": None,
                    "percent": 5,
                    "steam_item": True,
                    'nm': False
                }
            ]
        }
        result = steam_trader.Inventory.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_buy_orders(self):
        test_response = {
            "success": True,
            "data": [
                {
                    "id": 111,
                    "gid": 3,
                    "gameid": 440,
                    "hash_name": "Secret Saxton",
                    "date": 1507201426,
                    "price": 10,
                    "currency": 1,
                    "position": 0
                },
                {
                    "id": 92,
                    "gid": 3,
                    "gameid": 440,
                    "hash_name": "Secret Saxton",
                    "date": 1507137367,
                    "price": 123,
                    "currency": 1,
                    "position": 0
                }
            ]
        }
        result = steam_trader.BuyOrders.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_discounts(self):
        test_response = {
            "success": True,
            "data": {
                "753": {
                    "discount": 0,
                    "commission": 10,
                    "total_sell": 4.5,
                    "total_buy": 0
                },
                "730": {
                    "discount": 0,
                    "commission": 10,
                    "total_sell": 9,
                    "total_buy": 0
                },
                "440": {
                    "discount": 0,
                    "commission": 10,
                    "total_sell": 74.29,
                    "total_buy": 0
                },
                "570": {
                    "discount": 0,
                    "commission": 10,
                    "total_sell": 0,
                    "total_buy": 0
                }
            }
        }
        result = steam_trader.Discounts.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_operations_history(self):
        test_response = {
            "success": True,
            "data": [
                {
                    "id": 21,
                    "name": "Ящик от сообщества \"The End of the Line\" , тираж #87",
                    "type": 9,
                    "amount": 150,
                    "currency": 1,
                    "date": 1505126809
                },
                {
                    "id": 14,
                    "name": "Металлолом",
                    "type": 9,
                    "amount": 50,
                    "currency": 1,
                    "date": 1505126809
                }
            ]
        }
        result = steam_trader.OperationsHistory.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_inventory_state(self):
        test_response = {
            "success": True,
            "updatingNow": False,
            "lastUpdate": 1509898188,
            "itemsInCache": 9
        }
        result = steam_trader.InventoryState.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

    def test_alt_ws(self):
        test_response = {
            "success": True,
            "messages": [
                {
                    "type": 13,
                    "data": "{\"id\":1,\"price\":3.88,\"currency\":1,\"exchange_type\":\"bot\"}"
                }
            ]
        }
        result = steam_trader.AltWebSocket.de_json(test_response, client=self.client)
        self.assertion(test_response, result)

if __name__ == '__main__':
    unittest.main()
