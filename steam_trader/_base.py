import dataclasses
import logging
from abc import ABCMeta
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, Union

try:
    import ujson as json

    ujson = True
except ImportError:
    import json

if TYPE_CHECKING:
    from ._client import Client
    from ._client_async import ClientAsync

class TraderClientObject:
    """Базовый класс для всех объектов библиотеки."""

    __metaclass__ = ABCMeta

    @staticmethod
    def is_valid_model_data(data: Any, *, array: bool = False) -> bool:
        """Проверка на валидность данных.

        Args:
            data (:obj:`Any`): Данные для проверки.
            array (:obj:`bool`, optional): Является ли объект массивом.

        Returns:
            :obj:`bool`: Валидны ли данные.
        """
        if array:
            return data and isinstance(data, list) and all(isinstance(item, dict) for item in data)

        return data and isinstance(data, dict)

    @classmethod
    def de_json(cls: dataclass, data: dict, client: Union['Client', 'ClientAsync', None] = None) -> Optional[dict]:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (Union[:class:`steam_trader.Client`, :class:`steam_trader.ClientAsync`, :obj:`None`]): Клиент Steam Trader.

        Returns:
            :obj:`dict`, optional: Словарь с валидными аттрибутами для создания датакласса.
        """

        data = data.copy()

        fields = {f.name for f in dataclasses.fields(cls)}

        cleaned_data = {}
        unknown_data = {}

        for k, v in data.items():
            if k in fields:
                cleaned_data[k] = v
            else:
                unknown_data[k] = v

        if unknown_data:
            logging.warning(f'Были получены неизвестные аттриубты для класса {cls} :: {unknown_data}')

        return cleaned_data
