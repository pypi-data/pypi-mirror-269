from sqlexec.sql_support import get_table_select_sql
from typing import Sequence, Union, List, Tuple
from sqlexec.table_exec import get_condition_arg, get_where_arg_limit


class FieldWherePageExec:
    def __init__(self, field_where_exec, page_num, page_size):
        self.field_where_exec = field_where_exec
        self.page_num = page_num
        self.page_size = page_size

    def find(self):
        return self.field_where_exec.find_page(self.page_num, self.page_size)

    def query(self):
        return self.field_where_exec.query_page(self.page_num, self.page_size)

    def select(self):
        return self.field_where_exec.select_page(self.page_num, self.page_size)


class FieldWhereExec:
    def __init__(self, field_exec, **kwargs):
        self.field_exec = field_exec
        self.kwargs = kwargs

    def find(self):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').where(name='张三', age=55).find()
        """
        return self.field_exec.find(**self.kwargs)

    def find_one(self):
        """
        Return unique result(object) or None if no result.
        person = Person.fields('id', 'name', 'age').where(name='张三', age=55).find_one()
        """
        return self.field_exec.find_one(**self.kwargs)

    def query(self):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').where(name='张三', age=55).query()
        """
        return self.field_exec.query(**self.kwargs)

    def query_one(self):
        """
        Return unique result(dict) or None if no result.
        persons = Person.fields('id', 'name', 'age').where(name='张三', age=55).query_one()
        """
        return self.field_exec.query_one(**self.kwargs)

    def select(self):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').where(name='张三', age=55).select()
        """
        return self.field_exec.select(**self.kwargs)

    def select_one(self):
        """
        Return unique result(tuple) or None if no result.
        row = Person.fields('id', 'name', 'age').where(name='张三', age=55).select_one()
        """
        return self.field_exec.select_one(**self.kwargs)

    def find_page(self, page_num=1, page_size=10):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').where(name='张三', age=55).find_page(1, 10)
        :param page_num: page number
        :param page_size: page size
        """
        return self.field_exec.find_page(page_num, page_size, **self.kwargs)

    def query_page(self, page_num=1, page_size=10):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').where(name='张三', age=55).query_page(1, 10)
        :param page_num: page number
        :param page_size: page size
        """
        return self.field_exec.query_page(page_num, page_size, **self.kwargs)

    def select_page(self, page_num=1, page_size=10):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').where(name='张三', age=55).select_page(1, 10)
        :param page_num: page number
        :param page_size: page size
        """
        return self.field_exec.select_page(page_num, page_size, **self.kwargs)

    def page(self, page_num=1, page_size=10) -> FieldWherePageExec:
        return FieldWherePageExec(self, page_num, page_size)


class FieldPageExec:
    def __init__(self, field_exec, page_num=1, page_size=10):
        self.field_exec = field_exec
        self.page_num = page_num
        self.page_size = page_size

    def find(self, **kwargs):
        return self.field_exec.find_page(self.page_num, self.page_size, **kwargs)

    def query(self, **kwargs):
        return self.field_exec.query_page(self.page_num, self.page_size, **kwargs)

    def select(self, **kwargs):
        return self.field_exec.select_page(self.page_num, self.page_size, **kwargs)

    def where(self, **kwargs) -> FieldWherePageExec:
        return FieldWherePageExec(FieldWhereExec(self.field_exec, **kwargs), self.page_num, self.page_size)


class FieldExec:
    def __init__(self, cls, *fields):
        self.cls = cls
        self.fields = fields

    def find(self, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find(name='张三', age=55)
        """
        return self.cls.find(*self.fields, **kwargs)

    def find_one(self, **kwargs):
        """
        Return unique result(object) or None if no result.
        person = Person.fields('id', 'name', 'age').find_one(name='张三', age=55)
        """
        return self.cls.find_one(*self.fields, **kwargs)

    def find_by_id(self, _id: Union[int, str]):
        """
        Return one class object or None if no result.
        person = Person.fields('id', 'name', 'age').find_by_id(1)
        :param _id: key
        """
        return self.cls.find_by_id(_id, *self.fields)

    def find_by_ids(self, *ids):
        """
        Return list(class object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_by_ids(1,2)
        :param ids: List of key
        """
        return self.cls.find_by_ids(ids, *self.fields)

    def query(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query(name='张三', age=55)
        """
        return self.cls.query(*self.fields, **kwargs)

    def query_one(self, **kwargs):
        """
        Return unique result(dict) or None if no result.
        persons = Person.fields('id', 'name', 'age').query_one(name='张三', age=55)
        """
        return self.cls.query_one(*self.fields, **kwargs)

    def query_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        person = Person.fields('id', 'name', 'age').query_by_id(1)
        :param _id: key
        """
        return self.cls.query_by_id(_id, *self.fields)

    def query_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_by_ids(1,2)
        :param ids: List of key
        """
        return self.cls.query_by_ids(ids, *self.fields)

    def select(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select(name='张三', age=55)
        """
        return self.cls.select(*self.fields, **kwargs)

    def select_one(self, **kwargs):
        """
        Return unique result(tuple) or None if no result.
        row = Person.fields('id', 'name', 'age').select_one(name='张三', age=55)
        """
        return self.cls.select_one(*self.fields, **kwargs)

    def select_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        row = Person.fields('id', 'name', 'age').select_by_id(1)
        :param _id: key
        """
        return self.cls.select_by_id(_id, *self.fields)

    def select_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of key
        :param fields: Default select all fields if not set
        """
        return self.cls.select_by_ids(ids, *self.fields)

    def find_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.find_page(page_num, page_size, *self.fields, **kwargs)

    def query_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.query_page(page_num, page_size, *self.fields, **kwargs)

    def select_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self.cls.select_page(page_num, page_size, *self.fields, **kwargs)

    def where(self, **kwargs) -> FieldWhereExec:
        return FieldWhereExec(self, **kwargs)

    def page(self, page_num=1, page_size=10) -> FieldPageExec:
        return FieldPageExec(self, page_num, page_size)


class WherePageExec:
    def __init__(self, where_exec, page_num=1, page_size=10):
        self.where_exec = where_exec
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).page(1, 10).select()
        """
        return self.where_exec.select_page(self.page_num, self.page_size, *fields)

    def query(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).page(1, 10).query()
        """
        return self.where_exec.query_page(self.page_num, self.page_size, *fields)

    def find(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).page(1, 10).find()
        """
        return self.where_exec.find_page(self.page_num, self.page_size, *fields)

    def fields(self, *fields) -> FieldWherePageExec:
        return FieldWherePageExec(FieldWhereExec(FieldExec(self.where_exec.cls, *fields), **self.where_exec.kwargs), self.page_num, self.page_size)


class WhereExec:
    def __init__(self, cls, **kwargs):
        self.cls = cls
        self.kwargs = kwargs

    def delete(self):
        """
        Physical delete
        rowcount = Person.where(name='张三', age=55).delete()
        return: Effect rowcount
        """
        return self.cls.delete(**self.kwargs)

    def count(self):
        """
        count = Person.where(name='张三', age=55).count()
        """
        return self.cls.count(**self.kwargs)

    def exists(self):
        """
        flag = Person.where(name='张三', age=55).exists()
        """
        return self.cls.exists(**self.kwargs)

    def select(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).select()
        """
        return self.cls.select(*fields, **self.kwargs)

    def query(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).query()
        """
        return self.cls.query(*fields, **self.kwargs)

    def find(self, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).find()
        """
        return self.cls.find(*fields, **self.kwargs)

    def select_page(self, page_num=1, page_size=10, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).select_page()
        """
        return self.cls.select_page(page_num, page_size, *fields, **self.kwargs)

    def query_page(self, page_num=1, page_size=10, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).query_page()
        """
        return self.cls.query_page(page_num, page_size, *fields, **self.kwargs)

    def find_page(self, page_num=1, page_size=10, *fields):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where(name='张三', age=55).find_page()
        """
        return self.cls.find_page(page_num, page_size, *fields, **self.kwargs)

    def fields(self, *fields) -> FieldWhereExec:
        return FieldWhereExec(FieldExec(self.cls, *fields), **self.kwargs)

    def page(self, page_num=1, page_size=10) -> WherePageExec:
        return WherePageExec(self, page_num, page_size)


class PageExec:
    
    def __init__(self, cls, page_num=1, page_size=10):
        self.cls = cls
        self.page_num = page_num
        self.page_size = page_size

    def select(self, *fields, **kwargs):
        """
        Person.page(1, 10).select('id', 'name', 'age', name='张三', age=55)
        """
        return self.cls.select_page(self.page_num, self.page_size, *fields, **kwargs)

    def query(self, *fields, **kwargs):
        """
        Person.page(1, 10).query('id', 'name', 'age', name='张三', age=55)
        """
        return self.cls.query_page(self.page_num, self.page_size, *fields, **kwargs)

    def find(self, *fields, **kwargs):
        """
        Person.page(1, 10).query('id', 'name', 'age', name='张三', age=55)
        """
        return self.cls.find_page(self.page_num, self.page_size, *fields, **kwargs)

    def where(self, **kwargs) -> WherePageExec:
        return WherePageExec(WhereExec(self.cls, **kwargs), self.page_num, self.page_size)

    def fields(self, *fields) -> FieldPageExec:
        return FieldPageExec(FieldExec(self.cls, *fields), self.page_num, self.page_size)


def split_ids(ids: Sequence[int], batch_size):
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]


def get_table_name(class_name):
    for i in range(1, len(class_name) - 1)[::-1]:
        if class_name[i].isupper():
            class_name = class_name[:i] + '_' + class_name[i:]
    return class_name.lower()
