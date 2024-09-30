import bs4
import httpx
import logging
import functools
from collections.abc import Sequence, Callable
from typing import Optional, LiteralString, TypeVar, Any
from ._base import WebClientObject
from ._dataclasses import MainPage, ItemInfo, Referal, HistoryItem
from steam_trader import constants
from steam_trader.exceptions import Unauthorized, UnsupportedAppID


logging.getLogger(__name__).addHandler(logging.NullHandler())

F = TypeVar('F', bound=Callable[..., Any])

def log(method: F) -> F:
    logger = logging.getLogger(method.__module__)

    @functools.wraps(method)
    def wrapper(*args, **kwargs) -> Any:
        logger.debug(f'Entering: {method.__name__}')

        result = method(*args, **kwargs)
        logger.info(result)

        logger.debug(f'Exiting: {method.__name__}')

        return result

    return wrapper


class WebClient(WebClientObject):
    """Этот клиент позволяет получить данные сайта без API ключа или получить информацию, которая недоступна через API.
    Для некоторых методов необходимо указать ID сессии. Он находится в файлах куки (или хедерах) и переодически сбрасывается.

    Если вам не нравятся предупреждения об устаревании от httpx, то повысьте уровень логов модуля.
    Это не ошибка https://github.com/encode/httpx/discussions/2931.

    Args:
        sessionid (:obj:`int`), optional: ID сессии. Может быть пустым.
        proxy (:obj:`str`, optional): Прокси для запросов. Для использования нужен контекстный менеджер with.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
        **kwargs: Будут переданы httpx клиенту. Например timeout.

    Attributes:
        sessionid (:obj:`int`), optional: ID сессии.
        proxy (:obj:`str`, optional): Прокси для запросов.
        base_url (:obj:`str`, optional): Ссылка на API Steam Trader.
    """

    __slots__ = [
        'sessionid',
        'proxy',
        'base_utl'
    ]

    def __init__(
            self,
            sessionid: Optional[str] = None,
            *,
            proxy: Optional[str] = None,
            base_url: Optional[str] = None,
            **kwargs
    ):

        self.sessionid = sessionid

        if base_url is None:
            base_url = "https://steam-trader.com/"
        self.base_url = base_url

        self._httpx_client = None
        self.proxy = proxy
        self.kwargs = kwargs

    def __enter__(self) -> 'WebClient':
        self._httpx_client = httpx.Client(proxy=self.proxy, **self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._httpx_client.close()

    def get_main_page(
            self,
            gameid: int,
            *,
            price_from: int = 0,
            price_to: int = 2000,
            filters: dict[str, int] = None,
            text: Optional[str] = None,
            sort: LiteralString = '-rating',
            page: int = 1,
            items_on_page: int = 24
    ) -> 'MainPage':
        """Получить главную страницу покупки для игры.

        Args:
            gameid (:obj:`int`): AppID игры.
            price_from (:obj:`int`): Минимальная цена предмета.
            price_to (:obj:`int`): Максимальная цена предмета.
                Если больше или равно 2000, ограничение снимается.
            filters (:obj:`dict[str, int]`, optional): Словарь пар название/ID.
                См web_api.api.Filters для названий и web_api.constants для ID.
            text (:obj:`str`, optional): Текст, который должен встречаться в названии.
            sort (:obj:`LiteralString`): Метод сортировки.
                '-rating' - Сначала самые популярные. По умолчанию.
                'rating' - Сначала менее популярные.
                '-price' - Сначала самые дорогие.
                'price' - Сначала самые дешёвые.
                '-benefit' - Сначала самые невыгодные.
                'benefit' - Сначала самые выгодные.
                '-name' - В алфавитном порядке UNICODE.
                'name' - В обратном алфавитном порядке UNICODE.
            page (:obj:`int`): Номер страницы, начиная с 1.
            items_on_page (:obj:`int`): Кол-во отображаемых предметов на странице.
                Значение должно быть в диапазоне от 24 до 120 с интервалом 6.

        Returns:
            :class:`steam_trader.web_api.MainPage`: Главная страница покупки.
        """

        try:
            game_name = constants.NAME_BY_APPID[gameid]
        except KeyError:
            raise UnsupportedAppID('Указан недействительный AppID.')

        if items_on_page not in range(24, 121) or items_on_page % 6 != 0:
            logging.warning(f'Неправильное значение items_on_page >> {items_on_page}')

        if sort not in [None, '-rating', 'rating', '-price', 'price', '-benefit', 'benefit', '-name', 'name']:
            logging.warning(f'Неправильное значение sort >> {sort}')

        if filters is None:
            filters = {}

        url = self.base_url + game_name + '/'
        result = (self._httpx_client or httpx).get(
            url,
            headers={
                'x-pjax': 'true',
                'x-requested-with': 'XMLHttpRequest',
                'x-pjax-container': 'form.market .items .wrap'
            },
            params={
                'price_from': price_from,
                'price_to': price_to,
                **filters,
                'text': text,
                'sort': sort,
                'page': page,
            },
            cookies={
                'sid': self.sessionid,
                'settings': f'%7B%22market_{gameid}_onPage%22%3A{items_on_page}%7D'
            }
        ).json()

        return MainPage.de_json(result)

    def get_item_info(
            self,
            gid: int,
            *,
            page: int = 1,
            items_on_page: int = 24
    ) -> 'ItemInfo':
        """Получить информацию о предмете через WebAPI. Позволяет увидеть описание индивидуальных предметов.

        Args:
            gid (:obj:`int`): ID группы предметов.
            page (:obj:`int`): Номер страницы.
            items_on_page (:obj:`int`): Кол-во предметов на странице.
                Значение должно быть в диапазоне от 24 до 120 с интервалом 6.

        Returns:
            :class:`steam_trader.web_api.ItemInfo`: Информацию о предмете.
        """

        if items_on_page not in range(24, 121) or items_on_page % 6 != 0:
            logging.warning(f'Неправильное значение items_on_page >> {items_on_page}')

        url = f'{self.base_url}tf2/{gid}-The-Wrap-Assassin'  # Сайт перенаправляет на корректную страницу
        correct_url = (self._httpx_client or httpx).get(
            url,
            follow_redirects=True
        ).url

        result = (self._httpx_client or httpx).get(
            correct_url,
            headers={
                'x-pjax': 'true',
                'x-requested-with': 'XMLHttpRequest',
                'x-pjax-container': '#content #wrapper'
            },
            params={'page': page},
            cookies={
                'sid': self.sessionid,
                'settings': f'%7B%22item_onPage%22%3A{items_on_page}%7D'
            }
        ).json()

        return ItemInfo.de_json(result)

    def get_referral_link(self) -> str:
        """Получить реферальную ссылку.

        Returns:
            :obj:`str`: Реферальная ссылка.
        """

        if not self.sessionid:
            raise Unauthorized('Для использования данного метода нужно указать sessionid (sid). Вы можете найти его в файлах куки.')

        url = self.base_url + 'referral/'
        result = (self._httpx_client or httpx).get(
            url,
            headers={
                'x-pjax': 'true',
                'x-requested-with': 'XMLHttpRequest',
                'x-pjax-container': '#content #wrapper'
            },
            cookies={'sid': self.sessionid}
        ).json()

        html = bs4.BeautifulSoup(result['contents'], 'lxml')
        return html.find('input', {'class': 'big'}).get('value')

    def get_referals(
            self,
            status: Optional[int] = None,
            items_on_page: int = 24
    ) -> Sequence[Referal]:
        """Получить список рефералов.

        Args:
            status (:obj:`int`): Статус реферала.
                None - Все. По умолчанию.
                1 - Активный.
                2 - Пассивный.
            items_on_page (:obj:`int`): Кол-во рефералов на странице.
                Значение должно быть в диапазоне от 24 до 120.

        Returns:
            Sequence[:class:`steam_trader.web_api.Referal`]: Список рефералов.
        """

        if not self.sessionid:
            raise Unauthorized('Для использования данного метода нужно указать sessionid (sid). Вы можете найти его в файлах куки.')

        if items_on_page not in range(24, 121) or items_on_page % 6 != 0:
            logging.warning(f'Неправильное значение items_on_page >> {items_on_page}')

        url = self.base_url + 'referral/'
        result = (self._httpx_client or httpx).get(
            url,
            headers={
                'x-pjax': 'true',
                'x-requested-with': 'XMLHttpRequest',
                'x-pjax-container': '#content #wrapper'
            },
            params={'type': status},
            cookies={'sid': self.sessionid, 'settings': f'%7B%22referral_onPage%22%3A{items_on_page}%7D'}
        ).json()

        html = bs4.BeautifulSoup(result['contents'], 'lxml')
        tds = html.find_all('td')

        if tds[0].get('colspan') == '4':  # Ничего не найдено
            return []

        referals = []
        for td in tds:
            divs = td.find_all_next('div')
            data = {
                'name': divs[0].text,
                'date': divs[1].text,
                'status': divs[1].text,
                'sum': divs[1].text
            }
            referals.append(Referal.de_json(data))

        return referals

    def get_history_page(self, gameid: int, category: LiteralString = 'last_purchases') -> Sequence['HistoryItem']:
        """Получить страницу истории продаж.

        Args:
            gameid (:obj:`int`): AppID игры.
            category (:obj:`LiteralString`): Категория истории.
                'last_purchases': Последние покупки. По умолчанию.
                'day_most': Самые дорогие за 24 часа.
                'all_time_most': Самые дорогие за все время.

        Returns:
            Sequence[:class:`web_api.web_api.HistoryItem`]
        """

        try:
            game_name = constants.NAME_BY_APPID[gameid]
        except KeyError:
            raise UnsupportedAppID('Указан недействительный AppID.')

        match category:
            case 'last_purchases':
                i = 0
            case 'day_most':
                i = 1
            case 'all_time_most':
                i = 2
            case _:
                raise ValueError('Указано недопустимое значение category.')

        url = f'https://steam-trader.com/{game_name}/history/'
        page = (self._httpx_client or httpx).get(url)

        html = bs4.BeautifulSoup(page.content, 'lxml')

        history = html.find_all('div', {'class': 'items'})
        history_items = history[i].find_all('a')

        result = []
        for item in history_items:
            result.append(HistoryItem.de_json(item))
        return result
