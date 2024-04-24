"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
import datetime
import sqlite3
from joo.db.pep249 import Connection as _BaseConnection
import joo.db.sqlbuilder as sqlbuilder

class Connection(_BaseConnection):
    def __init__(self, **kwargs):
        _BaseConnection.__init__(self, **kwargs)

    def _open(self, **kwargs):
        try:
            params = {
                "database": kwargs.get("database"),
            }
            self.debug("Connecting database...")
            self.debug("database={}".format(params["database"]), 1)
            return sqlite3.connect(**params)
        except Exception as ex:
            self.exception(ex)
            return None

    def get_info(self, key):
        if key == "version": sql = "SELECT sqlite_version()"
        else: return None
        return self.query_value(sql)
    
    def list_tables(self):
        table_names = []
        rs = self.query("SELECT name FROM sqlite_master WHERE type='table'")
        if rs is None: return None
        for r in rs:
            if r[0] in ["sqlite_sequence"]: continue
            table_names.append(r[0])
        return table_names

def template_sql_insert(table_name, data_record, excludings=[]):
    return "INSERT INTO {} ({}) VALUES ({})".format(
        table_name,
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.backtick(key)), 
            data_record, excludings),
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.placeholder(key)), 
            data_record, excludings)
    )

def template_sql_insert_or_update(table_name, data_record,
                                  conflicts,
                                  excludings_update,
                                  excludings_insert=[]):
    def _f1(fields):
        parts = []
        for field in fields:
            parts.append(sqlbuilder.backtick(field))
        return ",".join(parts)

    def _f2(key, value):
        v = sqlbuilder.backtick(key)
        return "{}=EXCLUDED.{}".format(v, v)
    
    return "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT({}) DO UPDATE SET {}".format(
        table_name,
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.backtick(key)),
            data_record, excludings_insert),
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.placeholder(key)),
            data_record, excludings_insert),
        _f1(conflicts),
        sqlbuilder.parts_str(
            _f2,
            data_record, excludings_update)
    )

TEMPLATE_SQL_CREATE_TRIGGER_UPDATED_AT = """
CREATE TRIGGER IF NOT EXISTS "{trigger_name}"
AFTER UPDATE ON "{table_name}"
BEGIN
	UPDATE "{table_name}"
	SET `{updated_at}` = CURRENT_TIMESTAMP
	WHERE `{id}` = NEW.`{id}`;
END;
"""
def sql_create_trigger_updated_at(table_name,
                                  trigger_name,
                                  updated_at=None,
                                  id=None):
    params = {
        "table_name": table_name,
        "trigger_name": trigger_name,
        "updated_at": updated_at or "updated_at",
        "id": id or "id"
    }
    return TEMPLATE_SQL_CREATE_TRIGGER_UPDATED_AT.format(**params)

def escape_string(value):
    t = value.replace("'", "''")
    return t

def render_sql_with_values(template, data_record):
    r = {}
    for key, value in data_record.items():
        if value is None:
            r[key] = "NULL"
        elif type(value) == str:
            r[key] = sqlbuilder.quote(escape_string(value))
        elif type(value) == datetime.datetime:
            r[key] = sqlbuilder.quote(value.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            r[key] = value
    return template.format(**r)

