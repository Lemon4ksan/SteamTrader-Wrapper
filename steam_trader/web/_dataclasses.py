import json
import bs4
from lxml import etree
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional
from collections.abc import Sequence

from ._base import WebClientObject
from steam_trader.exceptions import UnknownItem, NotFoundError


@dataclass
class MainPageItem(WebClientObject):
    """Класс, представляющий данные предмета на главной странице.

    Attributes:
        benefit (:obj:`bool`): True, если цена ниже чем в steam.
        count (:obj:`int`): Кол-во предложений.
        description (:obj:`str`): Описание первого предмета.
        gid (:obj:`int`): ID группы предметов.
        hash_name (:obj:`str`): Параметр hash_name в steam.
        image_small (:obj:`str`): Неабсолютная ссылка на маленькое изображение.
        name (:obj:`str`): Переведённое название предмета.
        outline (:obj:`str`): HEX код цвета названия.
        price (:obj:`float`): Цена самого дешёвого предложения.
        type (:obj:`int`): Тип/Уровень предмета.
    """

    __slots__ = [
        'benefit',
        'count',
        'description',
        'gid',
        'hash_name',
        'image_small',
        'name',
        'outline',
        'price',
        'type'
    ]

    benefit: bool
    count: int
    description: str
    gid: int
    hash_name: str
    image_small: str
    name: str
    outline: str
    price: float
    type: str

    @classmethod
    def de_json(cls: dataclass, data: dict) -> 'MainPageItem':

        del data['color']
        data = super(MainPageItem, cls).de_json(data)

        return cls(**data)


@dataclass
class MainPage(WebClientObject):
    """Класс, представляющий главную страничку продажи.

    Attributes:
        auth (:obj:`bool`): Истина если был указан правильный sessionid (sid).
        items (Sequence[:class:`MainPageItem`]): Последовательность предметов.
        currency (:obj:`int`): Валюта. 1 - рубль.
        current_page (:obj:`int`): Текущая страница.
        page_count (:obj:`int`): Всего страниц.
        commission (:obj:`int`, optional): Коммиссия в %. Указывется если auth = True.
        discount (:obj:`float`): Скидка на покупки. Указывется если auth = True.
    """

    __slots__ = [
        'auth',
        'items',
        'currency',
        'current_page',
        'page_count',
        'commission',
        'discount'
    ]

    auth: bool
    items: Sequence['MainPageItem']
    currency: int
    current_page: int
    page_count: int
    commission: Optional[int]
    discount: Optional[float]

    @classmethod
    def de_json(cls: dataclass, data: dict) -> 'MainPage':

        try:
            _ = data['error']
            raise NotFoundError('По данному запросу предметов не найдено.')
        except KeyError:
            pass

        try:
            data['items'] = data['contents']['items']
        except TypeError:
            data['items'] = []
        del data['contents']

        for i, item in enumerate(data['items']):
            data['items'][i] = MainPageItem.de_json(item)

        del data['body'], data['chat'], data['handler'], data['menu'], data['sorter'], data['title'], data['game']

        try:
            _ = data['commission']
        except KeyError:
            data['commission'] = None

        try:
            _ = data['discount']
        except KeyError:
            data['discount'] = None

        data = super(MainPage, cls).de_json(data)

        return cls(**data)


@dataclass
class SellOffer(WebClientObject):
    """Класс, представляющий предложение о продаже.

    Attributes:
        id (:obj:`int`): Уникальный ID предложения.
        itemid (:obj:`int`): ID предмета.
        image_url (:obj:`str`): Неабсолютная ссылка на изображение предмета.
        name (:obj:`str`): Переведённое название предмета.
        type (:obj:`int`): Тип/Уровень предмета.
        price (:obj:`float`): Цена предложения.
    """

    __slots__ = [
        'id',
        'itemid',
        'image_url',
        'name',
        'type',
        'price'
    ]

    id: int
    itemid: int
    image_url: str
    name: str
    type: str
    price: float

    @classmethod
    def de_json(cls: dataclass, tag: 'bs4.Tag') -> 'SellOffer':

        tree = etree.HTML(str(tag))
        _type = tree.xpath('//div/table/tr/td[2]/div[2]/p[2]')[0].text

        data = {
            'id': int(tag.get('data-id')),  # Названия одинаковые, но это ID предложения
            'itemid': int(tree.xpath('//div')[0].get('data-id')),  # А это ItemID
            'image_url': tree.xpath('//div/table/tr/td[1]/img')[0].get('src'),
            'name': tree.xpath('//div/table/tr/td[2]/div[1]')[0].text,
            'type': _type if _type is not None else '',
            # 'effect': tree.xpath('//div/table/tr/td[2]/div[3]')[0].text,  # Без понятия что это
            'price': float(tree.xpath('//div/table/tr/td[4]/div')[0].get('data-price').replace('\xa0', ''))
        }
        return cls(**data)


@dataclass
class ItemDescription(WebClientObject):
    """Класс, представляющйи данные предмета."""

    name: str
    type: str
    image_small: str
    color: str
    outline: str
    description: str

    @classmethod
    def de_json(cls: dataclass, data: dict) -> 'ItemDescription':

        data = super(ItemDescription, cls).de_json(data)

        return cls(**data)

@dataclass
class ItemInfo(WebClientObject):
    """Класс, представляющий данные группы предметов.

    Attributes:
        auth (:obj:`bool`): Истина если был указан правильный sessionid (sid).
        sell_offers (Sequence[:class:`SellOffer`): Последовательность предложений о продаже. Только для текущей страницы.
        descriptions (Sequence[:obj:`dict[:obj:`int`, :class:`ItemDescription`]`]): Словарь с парами ItemID/описание.
            Только для текущей страницы. Если предмет типовой, равен None.
        item (:obj:`bool`): Истина если... если что?
        commission (:obj:`int`, optional): Коммиссия в %. Указывется если auth = True.
        discount (:obj:`float`): Скидка на покупки. Указывется если auth = True.
    """

    __slots__ = [
        'auth',
        'sell_offers',
        'descriptions',
        'item',
        'commission',
        'discount'
    ]

    auth: bool
    sell_offers: Sequence['SellOffer']
    descriptions: Optional[dict[int, ItemDescription]]
    item: bool
    commission: Optional[int]
    discount: Optional[float]

    @classmethod
    def de_json(cls: dataclass, data: dict) -> 'ItemInfo':

        html = bs4.BeautifulSoup(data['contents'], 'lxml')
        data['sell_offers'] = [SellOffer.de_json(tag) for tag in html.find_all('div', {'class': 'offer'})]

        try:
            script = html.find('script').text
            descriptions = dict(json.loads(script[script.index('var d=') + 6:script.index(';Market.setItemOffers(d,')]))
            for k, v in descriptions.copy().items():
                descriptions[int(k)] = ItemDescription.de_json(v)
                descriptions.pop(k)
        except ValueError:
            descriptions = None
        except AttributeError:
            raise UnknownItem('Неизвестный предмет.')

        data['descriptions'] = descriptions

        del data['title'], data['game'], data['menu'], data['contents']

        if 'commission' not in data:
            data['commission'] = None

        if 'discount' not in data:
            data['discount'] = None

        data = super(ItemInfo, cls).de_json(data)

        return cls(**data)


@dataclass
class Referal(WebClientObject):
    """Класс, представляющий реферала.

    Attributes:
        name (:obj:`str`): Имя рефералла.
        date (:obj:`str`): Дата присоединения.
        status (:obj:`str`): Статус реферала.
        sum (:obj:`float`): Сумма потраченных рефералом средств.
    """

    __slots__ = [
        'name',
        'date',
        'status',
        'sum'
    ]

    name: str
    date: str
    status: str
    sum: float

    @classmethod
    def de_json(cls: dataclass, data: dict) -> 'Referal':

        data = super(Referal, cls).de_json(data)

        return cls(**data)


@dataclass
class HistoryItem(WebClientObject):
    """Класс, представляющий предмет из истории продаж.

    Attributes:
        name (:obj:`str`): Название предмета.
        date (:obj:`str`): Отформатированная строка времени.
        price (:obj:`float`): Цена, за которую был продан предмет.
        color (:obj:`str`): HEX код цвета текста названия.
        image_url (:obj:`str`): Неабсолютная ссылка на изображение предмета.
    """

    __slots__ = [
        'name',
        'date',
        'price',
        'color',
        'image_url'
    ]

    name: str
    date: str
    price: float
    color: str
    image_url: str

    @classmethod
    def de_json(cls: dataclass, tag: bs4.Tag) -> 'HistoryItem':

        tree = etree.HTML(str(tag))

        data = {
            'image_url': tree.xpath('//span[1]/img')[0].get('src'),
            'price': float(tree.xpath('//span[2]')[0].text.replace('\xa0', '').replace(',', '.')),
            'date': tree.xpath('//span[3]')[0].text,
            'name': tree.xpath('//span[4]')[0].text,
            'color': tree.xpath('//span[4]')[0].get('style')[7:]
        }
        return cls(**data)
