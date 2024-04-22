from mysqlx.log_support import logger


def page_sql_id_log(function: str, sql_id: str, page_num, page_size, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.dbx.%s', page_num: %d, page_size: %d, sql_id: %s, args: %s, kwargs: %s" % (function, page_num, page_size, sql_id, args, kwargs))


def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func '%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def sql_id_select_key_log(function: str, select_key: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'sqlbatis.dbx.%s', select_key: %s, sql_id: %s, args: %s, kwargs: %s" % (function, select_key, sql_id.strip(), args, kwargs))
