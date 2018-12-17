# -*- coding: utf-8 -*-

import threading
import time
from typing import Optional
import requests


_interval: Optional[float] = None
_timer: Optional[threading.Thread] = None


def request(
        method: str,
        url: str,
        **kwargs) -> requests.Response:
    global _timer
    if _timer is not None:
        _timer.join()
        _timer = None
    response = requests.request(method, url, **kwargs)
    if _interval is not None:
        _timer = threading.Thread(
                name='pyatmo_request_interval_adjustment',
                target=time.sleep,
                args=(_interval,))
        _timer.start()
    return response


def interval(seconds: Optional[float]) -> None:
    global _interval
    _interval = seconds
