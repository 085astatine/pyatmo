# -*- coding: utf-8 -*-

import logging
import pathlib
from typing import Optional
import sqlalchemy
from ._device import Device, Module
from ._sqlalchemy import _DeclarativeBase
from .._client import Client


class Database:
    def __init__(
            self,
            path: pathlib.Path,
            client: Client,
            logger: Optional[logging.Logger] = None) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # client
        self._client = client
        # sqlalchemy engine
        self._engine = sqlalchemy.create_engine(
                'sqlite:///{0}'.format(path.as_posix()),
                encoding='utf-8')
        _DeclarativeBase.metadata.create_all(self._engine)
        # sqlalchemy session maker
        self._session_maker = sqlalchemy.orm.sessionmaker(bind=self._engine)

    def session(self, **kwargs) -> sqlalchemy.orm.session.Session:
        return self._session_maker(**kwargs)

    def register(
            self,
            device_id: Optional[str] = None,
            get_favorites: Optional[bool] = None) -> None:
        # request
        stations_data = self._client.get_stations_data(
                device_id=device_id,
                get_favorites=get_favorites)
        if stations_data is None:
            self._logger.error('stations data is none')
            return
        session = self.session()
        for device_data in stations_data['body']['devices']:
            # device
            device_argv = {
                    'id': device_data['_id'],
                    'name': device_data['station_name'],
                    'latitude': float(device_data['place']['location'][1]),
                    'longitude': float(device_data['place']['location'][0]),
                    'altitude': float(device_data['place']['altitude'])}
            device: Optional[Device] = (
                    session.query(Device)
                    .filter_by(id=device_argv['id']).one_or_none())
            if device is None:
                device = Device(**device_argv)
                session.add(device)
            else:
                for key, value in device_argv.items():
                    if key != 'id':
                        setattr(device, key, value)
            # main module
            main_module_argv = {
                    'id': device.id,
                    'device_id': device.id,
                    'name': device_data.get('module_name'),
                    'module_type': device_data['type'],
                    'data_type': ','.join(device_data['data_type'])}
            main_module: Optional[Module] = (
                    session.query(Module)
                    .filter_by(id=main_module_argv['id']).one_or_none())
            if main_module is None:
                main_module = Module(**main_module_argv)
                session.add(main_module)
            else:
                for key, value in main_module_argv.items():
                    if key != 'id':
                        setattr(main_module, key, value)
            # modules
            for module_data in device_data['modules']:
                module_argv = {
                        'id': module_data['_id'],
                        'device_id': device.id,
                        'name': module_data.get('module_name'),
                        'module_type': module_data['type'],
                        'data_type': ','.join(module_data['data_type'])}
                module: Optional[Module] = (
                    session.query(Module)
                    .filter_by(id=module_argv['id']).one_or_none())
                if module is None:
                    module = Module(**module_argv)
                    session.add(module)
                else:
                    for key, value in module_argv.items():
                        if key != 'id':
                            setattr(module, key, value)
        session.flush()
        session.commit()
        session.close()

    def unregister(self, device_id: str) -> None:
        session = self.session()
        device = session.query(Device).filter_by(id=device_id).one_or_none()
        if device is not None:
            session.delete(device)
            session.commit()
        session.close()

    def device(self, device_id: str) -> Optional[Device]:
        session = self.session()
        result: Optional[Device] = (
                session.query(Device)
                .filter_by(id=device_id).one_or_none())
        if result is not None:
            # load relationship
            result.modules
        session.close()
        return result
