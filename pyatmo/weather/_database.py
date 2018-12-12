# -*- coding: utf-8 -*-

import datetime
import logging
import re
import pathlib
from typing import Any, Dict, List, Optional, Tuple
import sqlalchemy
from ._sqlalchemy import SQLLogging, _DeclarativeBase
from ._table import Device, Measurements, Module
from .._client import Client


class Database:
    def __init__(
            self,
            path: pathlib.Path,
            client: Client,
            logger: Optional[logging.Logger] = None,
            sql_logging: SQLLogging = SQLLogging.NONE) -> None:
        # logger
        self._logger = logger or logging.getLogger(__name__)
        # client
        self._client = client
        # sqlalchemy engine
        self._engine = sqlalchemy.create_engine(
                'sqlite:///{0}'.format(path.as_posix()),
                encoding='utf-8',
                echo=sql_logging.sqlalchemy_echo())
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

    def update(self) -> None:
        session = self.session()
        timezone = datetime.datetime.now().astimezone().tzinfo
        for module in session.query(Module).all():
            self._logger.info('update module: {0}'.format(module.id))
            header = list(map(to_snake_case, module.data_type.split(',')))
            while True:
                # get latest timestamp
                latest_row: Optional[Tuple[int]] = (
                        session
                        .query(Measurements.timestamp)
                        .filter_by(module_id=module.id)
                        .order_by(Measurements.timestamp.desc())
                        .first())
                date_begin: Optional[int] = (
                        int(latest_row[0]) + 1
                        if latest_row is not None
                        else None)
                self._logger.info('update measurements from {0}'.format(
                        datetime.datetime.fromtimestamp(date_begin, timezone)
                        if date_begin is not None
                        else None))
                # request
                response = self._client.get_measure(
                        device_id=module.device_id,
                        module_id=module.id,
                        scale='max',
                        type_list=module.data_type.split(','),
                        date_begin=date_begin,
                        optimize=True)
                if response is None:
                    self._logger.error('get measure failed')
                    break
                # no latest data
                if len(response['body']) == 0:
                    self._logger.info('there is no latest measurement')
                    break
                # insert into
                for value_set in response['body']:
                    begin_time: int = value_set['beg_time']
                    step_time: int = value_set.get('step_time', 0)
                    for i, value in enumerate(value_set['value']):
                        data: Dict[str, Any] = {}
                        data['timestamp'] = begin_time + i * step_time
                        data['module_id'] = module.id
                        data.update(zip(header, value))
                        measurements = Measurements(**data)
                        session.add(measurements)
                session.flush()
                session.commit()
        session.close()

    def device(self, device_id: str) -> Optional[Device]:
        session = self.session()
        result: Optional[Device] = (
                session.query(Device)
                .options(sqlalchemy.orm.joinedload(Device.modules))
                .filter_by(id=device_id).one_or_none())
        session.close()
        return result

    def measurements(
            self,
            module: Module,
            begin_timestamp: Optional[int] = None,
            end_timestamp: Optional[int] = None) -> List[Measurements]:
        session = self.session()
        query = (session
                 .query(Measurements)
                 .filter_by(module_id=module.id)
                 .options(sqlalchemy.orm.joinedload(Measurements.module))
                 .order_by(Measurements.timestamp))
        if begin_timestamp is not None:
            query = query.filter(Measurements.timestamp >= begin_timestamp)
        if end_timestamp is not None:
            query = query.filter(Measurements.timestamp <= end_timestamp)
        result = query.all()
        session.close()
        return result


def to_snake_case(string: str) -> str:
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
