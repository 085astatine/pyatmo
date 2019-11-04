# -*- coding: utf-8 -*-

import threading
import time
from typing import Optional
import requests



class Request:
    _interval: Optional[float] = None
    _timer: Optional[threading.Thread] = None

    @classmethod
    def request(
            cls,
            method: str,
            url: str,
            **kwargs) -> requests.Response:
        if cls._timer is not None:
            cls._timer.join()
            cls._timer = None
        response = requests.request(method, url, **kwargs)
        if cls._interval is not None:
            cls._timer = threading.Thread(
                    name='pyatmo_request_interval_adjustment',
                    target=time.sleep,
                    args=(cls._interval,))
            cls._timer.start()
        return response

    @classmethod
    def interval(
            cls,
            seconds: Optional[float]) -> None:
        cls._interval = seconds


def request(
        method: str,
        url: str,
        **kwargs) -> requests.Response:
    return Request.request(method, url, **kwargs)


def interval(seconds: Optional[float]) -> None:
    Request.interval(seconds)
