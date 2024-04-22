from . import db
from sqlexec.sql_exec import SqlExec
from sqlexec.page_exec import PageExec


def sql(sql: str) :
    assert sql, "Parameter 'sql' must not be none"
    return SqlExec(db, sql)


def page(page_num: int, page_size: int) :
    return PageExec(db, page_num, page_size)
