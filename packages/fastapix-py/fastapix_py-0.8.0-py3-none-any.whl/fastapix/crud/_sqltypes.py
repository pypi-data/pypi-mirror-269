# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : _sqltypes.py
# @Time     : 2024/4/25 下午2:39
# @Desc     :
from sqlalchemy import types, Dialect
from sqlalchemy.dialects import postgresql


class AutoJson(types.TypeDecorator):
    impl = types.JSON
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> "types.TypeEngine[Any]":
        if dialect.name == "postgresql":
            return postgresql.JSONB(none_as_null=True)
        return types.JSON(none_as_null=True)
