import sqlite3
from sqlite3 import Connection
from sqlite3 import OperationalError
from typing import Optional

from src.db.exceptions import DatabaseInsertError
from src.db.exceptions import DatabaseUpdateError
from src.db.exceptions import DatabaseTableNameError
from src.db.exceptions import DatabaseConnectError
from src.settings.logging import logger
from src.db.statement import SqlStatement
from src.db.scopes import TableName


class DatabaseQuery:
    """
    Database query.

    При инициализации, по умолчанию в корне проекта создается файл db.sqlite
    для хранения БД.
    """

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.__instance = super(DatabaseQuery, cls).__new__(cls)
        return cls.__instance  # type: ignore

    def __init__(self,
                 uri: str = "db.sqlite") -> None:
        self._uri = uri
        self._connection: Connection = None  # type: ignore
        self._paramstyle = "named"

        # In serialized mode, SQLite can be safely used
        # by multiple threads with no restriction.
        # self._sql = sqlite3
        # self._sql.threadsafety = 1

        self._sql = SqlStatement()
        self.TABLE_NAME = TableName()
        self.is_connected = False
        self.ten_mil_sec = 0.1

    def __str__(self) -> str:
        return f"Connected to database in {self._uri}"

    def __repr__(self) -> str:
        return f"class DBHandler: paramstyle={self._paramstyle}"

    def __del__(self) -> None:
        logger.debug("Close database connection")
        self._connection.close()

    def connect(self) -> None:
        try:
            self._connection = sqlite3.connect(database=self._uri,
                                               check_same_thread=False)
        except Exception as err:
            msg = f"Unable to connect to the database, trace={err}"
            logger.exception(msg)
            raise DatabaseConnectError(msg)
        else:
            sqlite3.paramstyle = self._paramstyle
            self.is_connected = True
            logger.debug("Database connected")

    def reconnect(self) -> None:
        self._connection.close()
        self.connect()

    def create_all(self) -> None:
        self.create_table_object()
        self.create_table_config()
        self.create_table_page()
        logger.debug("All table is created")
        return

    def delete_all(self) -> None:
        self.delete_table_object()
        self.delete_table_config()
        self.delete_table_page()
        logger.debug("All table is deleted")
        return

    def create_table_object(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.CREATE_MAIN_OBJECT)
        self._connection.commit()
        cursor.close()

    def create_table_config(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.CREATE_MAIN_CONFIG)
        self._connection.commit()
        cursor.close()

    def create_table_page(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.CREATE_PAGE)
        self._connection.commit()
        cursor.close()

    def delete_table_object(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.DELETE_MAIN_OBJECT)
        self._connection.commit()
        cursor.close()

    def delete_table_config(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.DELETE_MAIN_CONFIG)
        self._connection.commit()
        cursor.close()

    def delete_table_page(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute(self._sql.DELETE_TABLE_PAGE)
        self._connection.commit()
        cursor.close()

    def insert_main_object(self,
                           row: Properties) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.INSERT_MAIN_OBJECT,
                           {"ouid": row.ouid,
                            "device": row.device,
                            "_type": row.type,
                            "_index": row.index,
                            "gateway": row.gateway,
                            "event": row.state.event,
                            "value": row.state.value,
                            "locked": int(row.state.locked),
                            "home": int(row.state.home),
                            "back": int(row.state.back),
                            "unconfigured": int(row.state.unconfigured)})
        except Exception as err:
            cursor.close()

            msg = f"Insert error, {err}"
            logger.exception(msg)
            raise DatabaseInsertError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("New row insert in table 'MainObject'")

    def insert_main_config(self,
                           row: Properties) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.INSERT_MAIN_CONFIG,
                           {"ouid": row.ouid,
                            "_offset": row.config.output[0].offset,
                            "raise_time": row.config.output[0].raise_time,
                            "fall_time": row.config.output[0].fall_time,
                            "_type": row.config.output[0].type,
                            "_mode": row.config.output[0].mode,
                            "_order": row.config.output[0].order,
                            "sacn_universe": row.config.output[0].universe,
                            "sacn_priority": row.config.sacn.priority,
                            "sacn_name": row.config.sacn.name,
                            "sacn_pps": row.config.sacn.pps,
                            "address": row.config.address})
        except Exception as err:
            cursor.close()

            msg = f"Insert error, {err}"
            logger.exception(msg)
            raise DatabaseInsertError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("New row insert in table 'MainConfig'")

    def insert_page(self,
                    ouid: str,
                    page: str) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.INSERT_PAGE,
                           {"ouid": ouid,
                            "page": page})
        except Exception as err:
            cursor.close()

            msg = f"Insert error, {err}"
            logger.exception(msg)
            raise DatabaseInsertError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("New row insert in table 'Page'")

    def update_main_object(self,
                           row: Properties) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.UPDATE_MAIN_OBJECT,
                           {"ouid": row.ouid,
                            "device": row.device,
                            "_type": row.type,
                            "_index": row.index,
                            "gateway": row.gateway,
                            "event": row.state.event,
                            "value": row.state.value,
                            "locked": int(row.state.locked),
                            "home": int(row.state.home),
                            "back": int(row.state.back),
                            "unconfigured": int(row.state.unconfigured)})
        except Exception as err:
            cursor.close()

            msg = f"Update error, {err}"
            logger.exception(msg)
            raise DatabaseUpdateError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("Row in MainObject is update")

    def update_main_config(self,
                           row: Properties) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.UPDATE_MAIN_CONFIG,
                           {"ouid": row.ouid,
                            "_offset": row.config.output[0].offset,
                            "raise_time": row.config.output[0].raise_time,
                            "fall_time": row.config.output[0].fall_time,
                            "_type": row.config.output[0].type,
                            "_mode": row.config.output[0].mode,
                            "_order": row.config.output[0].order,
                            "sacn_universe": row.config.output[0].universe,
                            "sacn_priority": row.config.sacn.priority,
                            "sacn_name": row.config.sacn.name,
                            "sacn_pps": row.config.sacn.pps,
                            "address": row.config.address})
        except Exception as err:
            cursor.close()

            msg = f"Update error, {err}"
            raise DatabaseUpdateError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("Row in MainConfig is update")

    def update_page(self,
                    ouid: str,
                    page: str) -> None:
        cursor = self._connection.cursor()

        try:
            cursor.execute(self._sql.UPDATE_PAGE,
                           {"ouid": ouid,
                            "page": page})
        except Exception as err:
            cursor.close()

            msg = f"Update error, {err}"
            raise DatabaseUpdateError(msg)
        else:
            self._connection.commit()
            cursor.close()

            logger.debug("Row in Page is update")

    def select(self,
               ouid: str,
               table: str) -> Optional[tuple]:

        if table == self.TABLE_NAME.OBJECT:
            statement = self._sql.SELECT_MAIN_OBJECT
        elif table == self.TABLE_NAME.CONFIG:
            statement = self._sql.SELECT_MAIN_CONFIG
        elif table == self.TABLE_NAME.PAGE:
            statement = self._sql.SELECT_PAGE
        else:
            msg = f"Table named={table} was not found in the database"
            logger.error(msg)
            raise DatabaseTableNameError(msg)

        cursor = self._connection.cursor()

        try:
            dbquery = cursor.execute(statement,
                                     {"ouid": ouid})
        except OperationalError as err:
            msg = f"Unable to connect to the database, trace={err}"
            logger.exception(msg)
            raise DatabaseConnectError(msg)
        else:
            dbquery = dbquery.fetchone()
        finally:
            cursor.close()

        if dbquery is None:
            return None
        else:
            return tuple(dbquery)
