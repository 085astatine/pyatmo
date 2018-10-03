# -*- coding: utf-8 -*-

import datetime
import logging
import pathlib
from typing import Any, Dict, List, Optional, Tuple
import requests
import yaml
from ._scope import Scope


__all__ = ['OAuth']


_token_url = 'https://api.netatmo.com/oauth2/token'


class OAuth:
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            scope_list: Optional[List[Scope]] = None,
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
        self._timezone = datetime.datetime.now().astimezone().tzinfo
        self._token_created_time: Optional[datetime.datetime] = None
        self._token_expiration_time: Optional[datetime.datetime] = None
        # scope
        self._scope_list: Optional[Tuple[Scope, ...]] = None
        if scope_list is not None and len(scope_list) != 0:
            self._scope_list = tuple(sorted(scope_list, key=lambda x: x.value))
        assert(self._scope_list is None or len(self._scope_list) != 0)
        # token file
        self._token_file = token_file
        if self._token_file is not None and self._token_file.exists():
            self.load_token(self._token_file)

    def get_access_token(
            self,
            username: str,
            password: str) -> None:
        self._logger.info('get access token')
        data = {'grant_type': 'password',
                'client_id': self._client_id,
                'client_secret': self._client_secret,
                'username': username,
                'password': password}
        if self._scope_list is not None:
            data['scope'] = ' '.join(map(str, self._scope_list))
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
                # token
                data['access_token'] = self._access_token
                data['refresh_token'] = self._refresh_token
                # time
                data['created_time'] = {
                        'timestamp': self._token_created_time.timestamp(),
                        'date': str(self._token_created_time)}
                data['expiration_time'] = {
                        'timestamp': self._token_expiration_time.timestamp(),
                        'date': str(self._token_expiration_time)}
                # scope
                if self._scope_list is not None:
                    data['scope_list'] = list(map(str, self._scope_list))
                yaml.dump(data, outfile, default_flow_style=False)
        else:
            self._logger.error('token is None')

    def load_token(self, path: pathlib.Path) -> None:
        self._logger.info('load token: {0}'.format(path))
        with path.open() as infile:
            data = yaml.load(infile)
            # scope match
            scope_list: Optional[Tuple[Scope, ...]] = (
                    tuple(sorted(
                            (scope for scope in Scope
                             if str(scope) in data['scope_list']),
                            key=lambda x: x.value))
                    if 'scope_list' in data
                    else None)
            if scope_list != self._scope_list:
                self._logger.error(
                        'scope mismatch: \'{0}\' (self) &  \'{1}\' (file)'
                        .format(', '.join(map(str, self._scope_list))
                                if self._scope_list is not None
                                else self._scope_list,
                                ', '.join(map(str, scope_list))
                                if scope_list is not None
                                else scope_list))
            assert(scope_list == self._scope_list)
            # token
            _set_token(self, data['access_token'], data['refresh_token'])
            # time
            self._token_created_time = (
                    datetime.datetime.fromtimestamp(
                            int(data['created_time']['timestamp']))
                    .replace(tzinfo=self._timezone))
            self._token_expiration_time = (
                    datetime.datetime.fromtimestamp(
                            int(data['expiration_time']['timestamp']))
                    .replace(tzinfo=self._timezone))

    def is_included(self, scope: Scope) -> bool:
        if self._scope_list is not None:
            return scope in self._scope_list
        else:
            return scope is Scope.default()

    @property
    def access_token(self) -> Optional[str]:
        # expiration check
        if (self._token_expiration_time is not None
                and (datetime.datetime.now(tz=self._timezone)
                     >= self._token_expiration_time)):
            self._logger.info('access token is expired')
            self.refresh_token()
        return self._access_token


def _update_token(self: OAuth, data: Dict[str, str]) -> None:
    _set_token(self, data['access_token'], data['refresh_token'])
    self._token_created_time = datetime.datetime.now().astimezone()
    self._token_expiration_time = (
            self._token_created_time
            + datetime.timedelta(seconds=int(data['expires_in'])))


def _set_token(self: OAuth, access_token: str, refresh_token: str) -> None:
    self._access_token = access_token
    self._refresh_token = refresh_token
