# -*- coding: utf-8 -*-

import sqlalchemy
from ._sqlalchemy import _DeclarativeBase


class Device(_DeclarativeBase):
    # table naame
    __tablename__ = 'devices'
    # column
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    latitude = sqlalchemy.Column(sqlalchemy.Float)
    longitude = sqlalchemy.Column(sqlalchemy.Float)
    altitude = sqlalchemy.Column(sqlalchemy.Float)
