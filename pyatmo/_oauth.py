# -*- coding: utf-8 -*-

import datetime
import logging
import pathlib
from typing import Any, Dict, List, Optional
import requests
import yaml


__all__ = ['OAuth']


_token_url = 'https://api.netatmo.com/oauth2/token'


class OAuth:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            token_file: Optional[pathlib.Path] = None,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # client
        self._client_id = client_id
        self._client_secret = client_secret
        # token
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        # time
        self._token_created_time: Optional[datetime.datetime] = None
        self._token_expiration_time: Optional[datetime.datetime] = None
        # token file
        self._token_file = token_file
        if self._token_file is not None and self._token_file.exists():
            self.load_token(self._token_file)

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
            _update_token(self, response.json())
            # save
            if self._token_file is not None:
                self.save_token(self._token_file)
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
                _update_token(self, response.json())
                # save
                if self._token_file is not None:
                    self.save_token(self._token_file)
            else:
                self._logger.error('refresh token: failed')
        else:
            self._logger.error('refresh token: token is None')

    def save_token(self, path: pathlib.Path) -> None:
        self._logger.info('save token: {0}'.format(path))
        if (self._access_token is not None
                and self._refresh_token is not None
                and self._token_created_time is not None
                and self._token_expiration_time is not None):
            with path.open(mode='w') as outfile:
                data: Dict[str, Any] = {}
                data['access_token'] = self._access_token
                data['refresh_token'] = self._refresh_token
                data['created_time'] = {
                        'timestamp': self._token_created_time.timestamp(),
                        'date': str(self._token_created_time)}
                data['expiration_time'] = {
                        'timestamp': self._token_expiration_time.timestamp(),
                        'date': str(self._token_expiration_time)}
                yaml.dump(data, outfile, default_flow_style=False)
        else:
            self._logger.error('token is None')

    def load_token(self, path: pathlib.Path) -> None:
        self._logger.info('load token: {0}'.format(path))
        with path.open() as infile:
            data = yaml.load(infile)
            self._access_token = data['access_token']
            self._refresh_token = data['refresh_token']
            self._token_created_time = datetime.datetime.fromtimestamp(
                    int(data['created_time']['timestamp'])).astimezone()
            self._token_expiration_time = datetime.datetime.fromtimestamp(
                    int(data['expiration_time']['timestamp'])).astimezone()

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token


def _update_token(self: OAuth, data: Dict[str, str]) -> None:
    self._access_token = data['access_token']
    self._refresh_token = data['refresh_token']
    self._token_created_time = datetime.datetime.now().astimezone()
    self._token_expiration_time = (
            self._token_created_time
            + datetime.timedelta(seconds=int(data['expires_in'])))
