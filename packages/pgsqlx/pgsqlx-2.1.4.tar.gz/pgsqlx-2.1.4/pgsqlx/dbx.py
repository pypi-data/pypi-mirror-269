from . import Dialect, db
from mysqlx import sql_holder as holder
from .log_support import sql_id_log, sql_id_key_seq_log
from sqlbatis.dbx import save_select_key, batch_execute, execute, get, query, query_one, select, select_one, select_page, query_page, sql, page


def save(sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_log('save', sql_id, *args, **kwargs)
    sql_model = holder.get_sql_model(sql_id)
    sql, args = holder.do_get_sql(sql_model, False, None, *args, **kwargs)
    select_key = Dialect.get_select_key(key_seq=sql_model.key_seq, sql=sql)
    return db.do_save_sql_select_key(select_key, sql, *args)


def save_key_seq(key_seq, sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_key_seq_log('save_key_seq', key_seq, sql_id, *args, **kwargs)
    sql_model = holder.get_sql_model(sql_id)
    sql, args = holder.get_sql(sql_model, False, None, *args, **kwargs)
    key_seq = key_seq if key_seq else sql_model.key_seq
    select_key = Dialect.get_select_key(key_seq=key_seq, sql=sql)
    return db.do_save_sql_select_key(select_key, sql, *args)

