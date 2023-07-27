# -*- coding:utf-8 -*-

from api.extensions import db
from api.lib.database import Model


class Hello(Model):
    __tablename__ = "hello"

    col_int = db.Column(db.Integer)
    col_text = db.Column(db.TEXT)
    col_varchar = db.Column(db.VARCHAR(64), index=True)
