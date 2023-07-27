# -*- coding:utf-8 -*-

from api.lib.mixin import DBMixin


class HelloCRUD(DBMixin):
    def _can_add(self, **kwargs):
        pass

    def _can_update(self, **kwargs):
        pass

    def _can_delete(self, **kwargs):
        pass
