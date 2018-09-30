#  -*- coding: utf-8 -*-

import logging
import pathlib
from typing import List, Optional
from ._oauth import OAuth
from ._scope import Scope


class Client:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            scope_list: Optional[List[Scope]] = None,
            token_file: Optional[pathlib.Path] = None,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # oauth
        self._oauth = OAuth(
                client_id,
                client_secret,
                scope_list=scope_list,
                token_file=token_file,
                logger=self._logger.getChild('oauth'))

    def authorize(
            self,
            username: str,
            password: str) -> None:
        self._oauth.get_access_token(username, password)
