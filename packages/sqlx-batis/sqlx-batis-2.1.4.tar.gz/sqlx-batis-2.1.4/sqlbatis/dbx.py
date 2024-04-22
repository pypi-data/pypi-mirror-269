from mysqlx import sql_holder as holder
from mysqlx.dbx import batch_execute, execute, get, query, query_one, select, select_one, select_page, query_page, sql, page

from . import db
from .log_support import logger, sql_id_log, page_sql_id_log, sql_id_select_key_log


def save(sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_log('save', sql_id, *args, **kwargs)
    sql_model = holder.get_sql_model(sql_id)
    select_key = sql_model.select_key
    sql, args = holder.do_get_sql(sql_model, False, None, *args, **kwargs)
    if select_key:
        return db.do_save_sql_select_key(select_key, sql, *args)
    return db.do_save_sql(sql, *args)


def save_select_key(select_key, sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_select_key_log('save_select_key', select_key, sql_id, *args, **kwargs)
    sql, args = holder.get_sql(sql_id, *args, **kwargs)
    return db.do_save_sql_select_key(select_key, sql, *args)


from .sql_id_exec import sql, page
