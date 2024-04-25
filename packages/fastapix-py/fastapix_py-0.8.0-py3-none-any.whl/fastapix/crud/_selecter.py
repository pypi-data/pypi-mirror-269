# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : zhangzhanqi
# @FILE     : _selecter.py
# @Time     : 2023/10/29 15:15
import re
from datetime import date, datetime
from re import Pattern
from typing import Optional, Type, Union, List, Tuple

from fastapi import Depends, Query  # noqa: F401
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from sqlalchemy import desc, cast, JSON, func, not_
from sqlmodel import SQLModel
from typing_extensions import Annotated

from fastapix.common.json import json_validator
from fastapix.common.pydantic import (
    model_fields, ModelField, Undefined,
    parse_date, parse_datetime,
    get_type_from_field,

)
from fastapix.crud._sqltypes import AutoJson


def get_modelfield_by_alias(table_model: Type[SQLModel], alias: str) -> Optional[ModelField]:
    fields = model_fields(table_model).values()
    for field in fields:
        if field.alias == alias or getattr(fields, 'serialization_alias', None) == alias:
            return field
    return None


def required_parser_str_set_list(primary_key: Union[int, str]) -> List[str]:
    if isinstance(primary_key, int):
        return [str(primary_key)]
    elif not isinstance(primary_key, str):
        return []
    return list(set(primary_key.split(",")))


RequiredPrimaryKeyListDepend = Annotated[List[str], Depends(required_parser_str_set_list)]


def parser_ob_str_set_list(order_by: Optional[str] = None) -> List[str]:
    return required_parser_str_set_list(order_by)


OrderByListDepend = Annotated[List[str], Depends(parser_ob_str_set_list)]

VisibleFieldsListDepend = Annotated[List[str], Depends(parser_ob_str_set_list)]


def get_python_type_parse(field: ModelField):
    try:
        python_type = get_type_from_field(field)
        if issubclass(python_type, date):
            if issubclass(python_type, datetime):
                return parse_datetime
            return parse_date
        return python_type
    except NotImplementedError:
        return str


def _mysql_python_to_table_json(value):
    value = json_validator(value)
    return cast(value, JSON)


def _python_to_table_json(value):
    value = json_validator(value)
    return cast(value, AutoJson)


def _is_json_type(python_type):
    return issubclass(python_type, (list, tuple, set, dict, BaseModel))


def equal_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[=]` : 等于, `abc` or `[=]abc`, 等于空字符串：`[=]`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        else:
            python_type = str
    value = python_type(value)
    return column.__eq__(value)


def not_equal_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[!=]` : 不等, `[!]abc` or `[!=]abc`, 不等于空字符串：`[!]` or `[!=]`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        else:
            python_type = str
    value = python_type(value)
    return column.__ne__(value)


def equal_null_query(
        column, value, python_type=str, dialect_type='sqlite'
) -> Tuple[Optional[str], Union[tuple, None]]:
    """
    `[?]` : 空值查询, `[=?]` or `[?]`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    return column.is_(None)


def not_equal_null_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[!?]` : 非空查询, `[!?]` or `[!=?]`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    return column.is_not(None)


def like_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[~]` : 模糊查询, like, `[~]abc`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type) or isinstance(python_type, str):
        value = f"%{value}%"
        return column.like(value)
    else:
        return None


def not_like_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[!~]` : 模糊查询, not like, `[!~]abc`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type) or isinstance(python_type, str):
        value = f"%{value}%"
        return column.not_like(value)
    else:
        return None


def in_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[*]` : 在范围内, in, `[*]abc,def,gh`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        else:
            python_type = str
    value = list(map(python_type, set(value.split(","))))
    return column.in_(value)


def not_in_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[!*]` : 不在范围内, not in, `[!*]abc,def,gh`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        else:
            python_type = str
    value = list(map(python_type, set(value.split(","))))
    return column.not_in(value)


def less_than_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[<]` : 小于, `[<]100`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        return None
    value = python_type(value)
    return column.__lt__(value)


def less_equal_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[<=]` : 小于等于, `[<=]100`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        return None
    value = python_type(value)
    return column.__le__(value)


def greater_than_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[>]` : 大于, `[>]100`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        return None
    value = python_type(value)
    return column.__gt__(value)


def greater_equal_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[>=]` : 大于等于, `[>=]100`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        return None
    value = python_type(value)
    return column.__ge__(value)


def between_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[-]` : 范围查询, between, `[-]100,300`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        return None
    value = value.split(",")[:2]
    if len(value) < 2:
        value = [0, *value]
    value = tuple(map(python_type, value))
    return column.between(*value)


def startswith_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[^]` : 以...开头, `[^]abc`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if isinstance(python_type, str):
        return column.startswith(value)
    else:
        return None


def endswith_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[$]` : 以...结尾, `[$]abc`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if isinstance(python_type, str):
        return column.endswith(value)
    else:
        return None


def regex_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[$]` : 以...结尾, `[$]abc`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if isinstance(python_type, str):
        return column.regexp_match(value)
    else:
        return None


def json_contains_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[@]` : Json包含, json_contains, `[@][abc,def,gh], 支持 mysql`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        value = python_type(value)

        if dialect_type in ['mysql']:
            return func.json_contains(column, value)
        if dialect_type in ['postgresql']:
            return func.jsonb_contains(column, value)
        else:
            return None
    else:
        return None


def not_json_contains_value_query(column, value, python_type=str, dialect_type='sqlite'):
    """
    `[!@]` : Json不包含, not json_contains, `[!@][abc,def,gh], 支持 mysql`
    :param column:
    :param value:
    :param python_type:
    :param dialect_type:
    :return:
    """
    if _is_json_type(python_type):
        if dialect_type in ['mysql', 'postgresql']:
            python_type = _python_to_table_json
        value = python_type(value)

        if dialect_type in ['mysql']:
            return not_(func.json_contains(column, value))
        if dialect_type in ['postgresql']:
            return not_(func.jsonb_contains(column, value))
        else:
            return None
    else:
        return None


sql_operator_pattern: Pattern = re.compile(r"^\[(=|<=|<|>|>=|!|!=|<>|\*|!\*|~|!~|-|\^|\$|#|\?|=\?|!\?|!=\?|@|!@)]")
sql_operator_map: dict = {
    "=": equal_value_query,
    "<=": less_equal_value_query,
    "<": less_than_value_query,
    ">": greater_than_value_query,
    ">=": greater_equal_value_query,
    "!": not_equal_value_query,
    "!=": not_equal_value_query,
    "<>": not_equal_value_query,
    "*": in_value_query,
    "!*": not_in_value_query,
    "~": like_value_query,
    "!~": not_like_value_query,
    "-": between_value_query,
    "^": startswith_value_query,
    "$": endswith_value_query,
    "#": regex_value_query,
    "?": equal_null_query,
    "=?": equal_null_query,
    "!?": not_equal_null_query,
    "!=?": not_equal_null_query,
    "@": json_contains_value_query,
    "!@": not_json_contains_value_query,
}
sql_operator_docs = """
## 查询条件示例：
`[=]` : 等于, `abc` or `[=]abc`, 等于空字符串：`[=]`

`[!=]` : 不等, `[!]abc` or `[!=]abc`, 不等于空字符串：`[!]` or `[!=]`

`[?]` : 空值查询, `[=?]` or `[?]`

`[!?]` : 非空查询, `[!?]` or `[!=?]`

`[~]` : 模糊查询, like, `[~]abc`

`[!~]` : 模糊查询, not like, `[!~]abc`

`[*]` : 在范围内, in, `[*]abc,def,gh`

`[!*]` : 不在范围内, not in, `[!*]abc,def,gh`

`[@]` : Json包含, json_contains, `[@][abc,def,gh], 支持 mysql`

`[!@]` : Json不包含, not json_contains, `[!@][abc,def,gh], 支持 mysql`

`[<]` : 小于, `[<]100`

`[<=]` : 小于等于, `[<=]100`

`[>]` : 大于, `[>]100`

`[>=]` : 大于等于, `[>=]100`

`[-]` : 范围查询, between, `[-]100,300`

`[^]` : 以...开头, `[^]abc`

`[$]` : 以...结尾, `[$]abc`

`[#]` : 正则查询, `[#]regex`

## 排序

`+` : 正序, `create_time` or `+create_time`

`-` : 倒序, `-create_time`

`,` : 多字段, `create_time,-id`
"""


class Selector:
    Model: Type[SQLModel]

    def __call__(self, *args, **kwargs):
        pass

    def calc_filter_clause(self, dialect_type='sqlite'):
        queries = []
        errors = []
        for name, value in self.__dict__.items():
            if value:
                model_field = model_fields(self.Model).get(name, None)
                python_type = get_python_type_parse(model_field)
                column = getattr(self.Model, name)

                try:
                    match = sql_operator_pattern.match(value)
                    op_key = match.group(1) if match else '='
                    query_func = sql_operator_map.get(op_key)
                    value = value.replace(f"[{op_key}]", "")
                    query = query_func(column, value, python_type, dialect_type)
                    if query is not None:
                        queries.append(query)
                except ValueError as e:
                    errors.append(
                        {
                            "type": "type_error",
                            "loc": ("query", name),
                            "msg": "JSON decode error",
                            "input": f"Input should be a valid {python_type}, invalid {value}",
                            "ctx": {"error": e},
                        }
                    )
        if errors:
            raise RequestValidationError(errors)
        return queries


class Paginator:
    def __init__(
            self,
            page: int = 1,
            page_size: int = None,
            show_total: bool = True,
            order_by: OrderByListDepend = None,
    ):
        self.page = page
        self.page_size = page_size
        self.show_total = show_total
        self.order_by = order_by

    def calc_ordering(self):
        order = []
        for ob in self.order_by:
            if isinstance(ob, str) and ob.startswith("-"):
                order.append(desc(ob[1:]))
            elif isinstance(ob, str) and ob.startswith("+"):
                order.append(ob[1:])
            else:
                order.append(ob)

        return order


def sqlmodel_to_selector(
        base_model: Type[SQLModel],
) -> Type[Selector]:
    imports = ['from fastapi import Query']
    params = []
    methods = []
    for name, field in model_fields(base_model).items():
        field_info = field.field_info
        if getattr(field_info, 'query', False) is False:
            continue
        if getattr(field_info, 'primary_key', False) is True:
            params.append(f"{name}: str = Query(None, alias='primary_key', "
                          f"description='`{base_model.__name__}.{name}`: 主键')")
            methods.append(f"self.{name} = {name}")
        else:
            params.append(
                f"""{name}: str = Query(None,
                    gt={getattr(field_info, 'gt', None)},
                    ge={getattr(field_info, 'ge', None)},
                    lt={getattr(field_info, 'lt', None)},
                    le={getattr(field_info, 'le', None)},
                    min_length={getattr(field_info, 'min_length', None)},
                    max_length={getattr(field_info, 'max_length', None)},
                    max_digits={getattr(field_info, 'max_digits', Undefined)},
                    decimal_places={getattr(field_info, 'decimal_places', Undefined)},
                  description="`{base_model.__name__}.{name}`: {field_info.title}")"""
            )
            methods.append(f"self.{name} = {name}")
    func = f"""
{";".join(set(imports))}
def call(
    self,
    {",".join(set(params))}
):
    {";".join(set(methods))}
    return self
    """
    exec(func, globals())

    return type(
        f'{base_model.__name__}Selector',
        (Selector,),
        {
            'Model': base_model,
            '__call__': call  # type: ignore
        }
    )
