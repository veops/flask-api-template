# -*- coding:utf-8 -*-

from flask_login.mixins import UserMixin


class User(UserMixin):
    def __init__(self, uid, username, nickname):
        self.id = uid
        self.uid = uid
        self.username = username
        self.nickname = nickname or username
