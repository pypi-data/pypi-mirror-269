"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
import datetime
import pymysql
from joo.db.pep249 import Connection as _BaseConnection
import joo.db.sqlbuilder as sqlbuilder

class Connection(_BaseConnection):
    def __init__(self, **kwargs):
        _BaseConnection.__init__(self, **kwargs)

    def _open(self, **kwargs):
        try:
            params = {
                "host": kwargs.get("host", "localhost"),
                "port": kwargs.get("port", 3306),
                "user": kwargs.get("user", "root"),
                "password": kwargs.get("password", ""),
                "database": kwargs.get("database"),
                "charset": kwargs.get("charset", "utf8")
            }
            self.debug("Connecting database...")
            self.debug("host={} port={} user={} database={}".format(
                params["host"],
                params["port"],
                params["user"],
                params["database"]), 1)
            return pymysql.connect(**params)
        except Exception as ex:
            self.exception(ex)
            return None

    def _reconnect_on_error(self, ex):
        # check error
        if type(ex) == pymysql.OperationalError:
            errcode = ex.args[0]
            if errcode not in [2006, 2013]: return False
        elif type(ex) == pymysql.err.InterfaceError:
            pass
        else: return False

        # reconnect
        return self.reopen() is not None

    def get_info(self, key):
        if key == "version": sql = "SELECT VERSION()"
        elif key == "os": sql = "SELECT @@version_compile_os"
        elif key == "basedir": sql = "SELECT @@basedir"
        elif key == "datadir": sql = "SELECT @@datadir"
        elif key == "database": sql = "SELECT DATABASE()"
        elif key == "user": sql = "SELECT USER()"
        elif key == "connections": sql = "SHOW STATUS WHERE variable_name='Threads_connected'"
        else: return None
        return self.query_value(sql)
    
    def list_databases(self):
        return self.query_values("SHOW DATABASES;")
    
    def list_tables(self, database_name=None):
        table_names = []
        if database_name is None:
            db_names = self.list_databases()
            if db_names is None: return None
            for db_name in db_names:
                if db_name in ["sys", "mysql", "information_schema", "performance_schema"]: continue
                t = self.list_tables(db_name)
                if t is None: return None
                table_names += t
        else:
            rs = self.query("SHOW TABLES IN {}".format(database_name))
            if rs is None: return None
            for r in rs:
                table_names.append(database_name + "." + r[0])
        return table_names
    
    def list_processes(self, user=None):
        sql = "SELECT user, host, db, command, time, state "
        sql += "FROM information_schema.processlist"
        rs = self.query(sql)
        if rs is None: return None
        results = []
        for r in rs:
            if user:
                if r[0] != user: continue
            results.append({
                "user": r[0],
                "host": r[1],
                "db": r[2],
                "command": r[3],
                "time": r[4],
                "state": r[5]
            })
        return results

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

def template_sql_replace(table_name, data_record, excludings=[]):
    return "REPLACE INTO {} ({}) VALUES ({})".format(
        table_name,
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.backtick(key)), 
            data_record, excludings),
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.placeholder(key)), 
            data_record, excludings)
    )

def template_sql_insert_or_update(table_name, data_record,
                                  excludings_update,
                                  excludings_insert=[]):
    def _f(key, value):
        v = sqlbuilder.backtick(key)
        return "{}=VALUES({})".format(v, v)
    
    return "INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}".format(
        table_name,
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.backtick(key)),
            data_record, excludings_insert),
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.placeholder(key)),
            data_record, excludings_insert),
        sqlbuilder.parts_str(
            _f,
            data_record, excludings_update)
    )

def template_sql_insert_or_update_v8(table_name, data_record,
                                     excludings_update,
                                     excludings_insert=[]):
    def _f(key, value):
        v = sqlbuilder.backtick(key)
        return "{}=t.{}".format(v, v)
    
    # https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html
    return "INSERT INTO {} ({}) VALUES ({}) as t ON DUPLICATE KEY UPDATE {}".format(
        table_name,
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.backtick(key)),
            data_record, excludings_insert),
        sqlbuilder.parts_str(
            (lambda key, value: sqlbuilder.placeholder(key)),
            data_record, excludings_insert),
        sqlbuilder.parts_str(
            _f,
            data_record, excludings_update)
    )

def render_sql_with_values(template, data_record):
    r = {}
    for key, value in data_record.items():
        if value is None:
            r[key] = "NULL"
        elif type(value) == str:
            r[key] = sqlbuilder.quote(pymysql.converters.escape_string(value))
        elif type(value) == datetime.datetime:
            r[key] = sqlbuilder.quote(value.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            r[key] = value
    return template.format(**r)

