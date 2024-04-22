from mysqlx import sql_support
# Don't remove. Import for not repetitive implementation
from sqlexec import save_select_key, do_save_sql_select_key
from mysqlx.db import insert, save, execute, batch_insert, batch_execute, get, query, query_one, select, select_one, \
    do_execute, do_get, do_query, do_query_one, do_select, do_select_one, do_select_page, do_query_page, select_page, query_page,\
    do_save_sql, drop_table, truncate_table, sql, table, page


def save_sql(sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.save_sql', sql, *args, **kwargs)
    return do_save_sql(sql, *args)


def save_sql_select_key(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql, args = sql_support.try_dynamic_sql('sqlbatis.db.save_sql', sql, *args, **kwargs)
    return do_save_sql_select_key(select_key, sql, *args)


from .sql_page_exec import sql, page
