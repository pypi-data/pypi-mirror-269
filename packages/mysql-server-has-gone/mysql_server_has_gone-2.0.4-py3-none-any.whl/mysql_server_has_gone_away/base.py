"""
https://stackoverflow.com/a/60894948/3872976
"""

import logging

from django.db import IntegrityError, InterfaceError, OperationalError
from django.db.backends.mysql import base
from django.db.utils import OperationalError as DjangoOperationalError
from MySQLdb import OperationalError as MySQLOperationalError
from retry import retry

logger = logging.getLogger("mysql_server_has_gone_away")


def check_mysql_gone_away(db_wrapper):
    def decorate(f):
        @retry(tries=5)
        def wrapper(self, query, args=None):
            try:
                return f(self, query, args)
            except (OperationalError, DjangoOperationalError, MySQLOperationalError, InterfaceError) as e:
                logger.error(f"MySQL server has gone away. Rerunning query: {query}; Error: {e}")
                if (
                    "MySQL server has gone away" in str(e)
                    or "Server has gone away" in str(e)
                    or "Lost connection to MySQL server during query" in str(e)
                    or "The client was disconnected by the server because of inactivity" in str(e)
                ):
                    db_wrapper.connection.close()
                    db_wrapper.connect()
                    self.cursor = db_wrapper.connection.cursor()
                    return f(self, query, args)
                # Map some error codes to IntegrityError, since they seem to be
                # misclassified and Django would prefer the more logical place.
                if e.args[0] in self.codes_for_integrityerror:
                    raise IntegrityError(*tuple(e.args))
                raise

        return wrapper

    return decorate


class DatabaseWrapper(base.DatabaseWrapper):

    def create_cursor(self, name=None):

        class CursorWrapper(base.CursorWrapper):

            @check_mysql_gone_away(self)
            def execute(self, query, args=None):
                return self.cursor.execute(query, args)

            @check_mysql_gone_away(self)
            def executemany(self, query, args):
                return self.cursor.executemany(query, args)

        cursor = self.connection.cursor()
        return CursorWrapper(cursor)

    def _set_autocommit(self, autocommit):
        try:
            super()._set_autocommit(autocommit)
        except (DjangoOperationalError, MySQLOperationalError) as e:
            logger.error(f"DatabaseWrapper Error: {e}")
