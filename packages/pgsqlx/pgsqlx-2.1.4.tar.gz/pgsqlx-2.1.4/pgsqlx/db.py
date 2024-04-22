from . import Dialect
from .log_support import save_log, save_key_seq_log

# Don't remove. Import for not repetitive implementation
from sqlbatis.db import insert, save, save_select_key, execute, batch_insert, batch_execute, get, query, query_one, select, select_one, save_sql, \
    save_sql_select_key, do_execute, do_get, do_query, do_query_one, do_select, do_select_one, do_select_page, do_query_page, select_page, query_page,\
    do_save_sql, do_save_sql_select_key, drop_table, drop_table, sql, table, page


def save_key_seq(key_seq: str, table_name: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param key_seq: primary key sequnece
    :param table_name: table
    :param kwargs:
    :return: Primary key
    """
    save_key_seq_log(key_seq, table_name, **kwargs)
    return save_select_key(Dialect.get_select_key(key_seq=key_seq), table_name, **kwargs)


def save_sql_key_seq(key_seq: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param key_seq: primary key sequnece
    :param sql: SQL
    :param kwargs:
    :return: Primary key
    """
    return save_sql_select_key(Dialect.get_select_key(key_seq=key_seq), sql, *args, **kwargs)
