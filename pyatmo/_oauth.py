# -*- coding: utf-8 -*-

import logging
from typing import List, Optional
import requests


_token_url = 'https://api.netatmo.com/oauth2/token'


class OAuth:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # client
        self._client_id = client_id
        self._client_secret = client_secret
        # token
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None

    def get_access_token(
            self,
            username: str,
            password: str,
            scope_list: List[str]) -> None:
        self._logger.info('get access token')
        data = {'grant_type': 'password',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'username': username,
                'password': password,
                'scope': ' '.join(scope_list)}
        response = requests.post(_token_url, data=data)
        if response.ok:
            self._logger.info('get access token: success')
            result = response.json()
            self._access_token = result['access_token']
            self._refresh_token = result['refresh_token']
        else:
            self._logger.error('get access token: failed')

    def refresh_token(self) -> None:
        self._logger.info('refresh token')
        if self._refresh_token is not None:
            self._logger.info('refresh token: success')
            data = {'grant_type': 'refresh_token',
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                    'refresh_token': self._refresh_token}
            response = requests.post(_token_url, data=data)
            if response.ok:
                result = response.json()
                self._access_token = result['access_token']
                self._refresh_token = result['refresh_token']
            else:
                self._logger.error('refresh token: failed')
        else:
            self._logger.error('refresh token: token is None')

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token
