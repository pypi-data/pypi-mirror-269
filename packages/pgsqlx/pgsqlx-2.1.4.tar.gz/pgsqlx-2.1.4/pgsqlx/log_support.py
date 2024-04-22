from sqlbatis.log_support import logger


def save_log(table, **kwargs):
    logger.debug("Exec func 'pgsqlx.db.save' \n\t Table: '%s', kwargs: %s" % (table, kwargs))


def sql_id_log(function: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'pgsqlx.dbx.%s', sql_id: %s, args: %s, kwargs: %s" % (function, sql_id.strip(), args, kwargs))


def save_key_seq_log(key_seq: str, table: str, **kwargs):
    logger.debug("Exec func 'pgsqlx.db.save_key_seq', key_seq: '%s' \n\t Table: '%s', kwargs: %s" % (key_seq, table, kwargs))


def sql_id_key_seq_log(function: str, key_seq: str, sql_id: str, *args, **kwargs):
    logger.debug("Exec func 'pgsqlx.dbx.%s', key_seq: %s, sql_id: %s, args: %s, kwargs: %s" % (function, key_seq, sql_id.strip(), args, kwargs))

def orm_insert_log(function, class_name, **kwargs):
    logger.debug("Exec func 'pgsqlx.orm.Model.%s' \n\t Class: '%s', kwargs: %s" % (function, class_name, kwargs))
