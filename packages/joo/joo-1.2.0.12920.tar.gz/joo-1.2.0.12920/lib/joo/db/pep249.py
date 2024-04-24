"""
    This file is part of joo library.
    :copyright: Copyright 1993-2024 Wooloo Studio.  All rights reserved.
    :license: MIT, check LICENSE for details.
"""
from joo.db import Connection as _BaseConnection

class Connection(_BaseConnection):
    """Base class of database access solution based on PEP249.
    Python Database API Specification v2.0
    https://peps.python.org/pep-0249/
    """
    def __init__(self, **kwargs):
        _BaseConnection.__init__(self, **kwargs)

        # settings
        self._log_operation = kwargs.get("log_operation", False)
        self._commit_before_execute = kwargs.get("commit_before_execute", True)
        self._operation_language = "SQL"

    def _close(self, handle):
        try:
            self.debug("Disconnecting database...")
            handle.close()
        except Exception as ex:
            self.exception(ex)

    def _reconnect_on_error(self, ex): return False

    def _execute(self,
                 op_or_ops,
                 commit_before_execute,
                 commit_after_execute,
                 fetch_rows,
                 auto_reconnect):
        # check op/ops
        if isinstance(op_or_ops, str): op_list = [op_or_ops]
        elif isinstance(op_or_ops, list): op_list = op_or_ops
        elif isinstance(op_or_ops, tuple): op_list = op_or_ops
        else: return None
        if len(op_list) == 0: return None

        # get connection
        connection = self.handle
        if connection is None: return None

        # execute
        cursor = None
        try:
            # commit before execute
            if commit_before_execute: connection.commit()

            # open cursor
            cursor = connection.cursor()
            
            # execute
            for operation in op_list:
                if self._log_operation:
                    self.debug("Executing {}...".format(self._operation_language))
                    self.debug(operation, 1)
                affected_rows = cursor.execute(operation)
            
            # commit after execute
            if commit_after_execute: connection.commit()

            # get result
            return_cursor = False
            if fetch_rows is None:
                result = cursor
                return_cursor = True
            elif fetch_rows < 0:
                result = affected_rows  # from last execute
            elif fetch_rows == 0:
                result = cursor.fetchall()
            else:
                result = cursor.fetchmany(fetch_rows)
            
            # close cursor
            if not return_cursor: cursor.close()
            cursor = None

            #
            return result
        except Exception as ex:
            self.exception(ex)
            if cursor:
                connection.rollback()
                cursor.close()
            if not auto_reconnect: return None
            if not self._reconnect_on_error(ex): return None
            return self._execute(
                op_or_ops,
                commit_before_execute,
                commit_after_execute,
                fetch_rows,
                auto_reconnect=False
            )
    
    def execute(self, op_or_ops, commit=True):
        return self._execute(
            op_or_ops,
            commit_before_execute=False,
            commit_after_execute=commit,
            fetch_rows=-1,
            auto_reconnect=True
        )
    
    def query(self, op, fetch_rows=0):
        return self._execute(
            op,
            commit_before_execute=self._commit_before_execute,
            commit_after_execute=False,
            fetch_rows=fetch_rows,
            auto_reconnect=True
        )
    
    def query_one(self, op):
        rs = self.query(op, 1)
        if rs is None: return None
        if len(rs) < 1: return None
        return rs[0]
    
    def query_value(self, op):
        r = self.query_one(op)
        if r is None: return None
        return r[0]
    
    def query_values(self, op):
        rs = self.query(op)
        if rs is None: return None
        values = []
        for r in rs: values.append(r[0])
        return values
