import typing as tp

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retry_strat = Retry(
            total=self.max_retries, backoff_factor=self.backoff_factor, status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strat)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        url = "/" + url
        response = session.get(
            url=self.base_url + url, timeout=kwargs["timeout"] if "timeout" in kwargs else self.timeout
        )
        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        retry_strat = Retry(
            total=self.max_retries, backoff_factor=self.backoff_factor, status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strat)
        session = requests.Session()
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        url = "/" + url
        response = session.post(url=self.base_url + url, data=kwargs)
        return response
