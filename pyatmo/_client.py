#  -*- coding: utf-8 -*-

import logging
import pathlib
from typing import Optional
from ._oauth import OAuth


class Client:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            token_file: Optional[pathlib.Path] = None,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # oauth
        self._oauth = OAuth(
                client_id,
                client_secret,
                token_file=token_file,
                logger=self._logger.getChild('oauth'))

    def authorize(
            self,
            username: str,
            password: str) -> None:
        self._oauth.get_access_token(username, password, ['read_station'])
