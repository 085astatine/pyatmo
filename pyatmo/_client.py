#  -*- coding: utf-8 -*-

import logging
import pathlib
from typing import Any, Dict, List, Optional
import requests
from ._oauth import CredentialFilter, OAuth
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
        for handler in self._logger.handlers:
            handler.addFilter(CredentialFilter())
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

    def get_stations_data(
            self,
            device_id: Optional[str] = None,
            get_favorites: Optional[bool] = None) -> Optional[Dict[str, Any]]:
        self._logger.info('get stations data')
        if not self._oauth.is_included(Scope.READ_STATION):
            self._logger.error('get stations data: failure')
            self._logger.error('dose not have good scope rights')
            return None
        url = 'https://api.netatmo.com/api/getstationsdata'
        data: Dict[str, Any] = {}
        data['access_token'] = self._oauth.access_token
        if device_id is not None:
            data['device_id'] = device_id
        if get_favorites is not None:
            data['get_favorites'] = get_favorites
        self._logger.debug('data: {0}'.format(data))
        response = requests.post(url, data=data)
        if response.ok:
            self._logger.info('get stations data: success')
            self._logger.debug('status_code: {0}'.format(response.status_code))
            self._logger.debug('text: {0}'.format(response.text))
            return response.json()
        else:
            self._logger.error('get stations data: failure')
            self._logger.error('status_code: {0}'.format(response.status_code))
            self._logger.error('text: {0}'.format(response.text))
            return None
