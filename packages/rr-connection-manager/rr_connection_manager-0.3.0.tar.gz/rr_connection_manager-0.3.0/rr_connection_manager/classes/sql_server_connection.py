import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .connection import Connection


class SQLServerConnection(Connection):
    def __init__(self, app=None) -> None:
        super().__init__(app)
        self._connection_details = self._set_details()

    def _set_details(self):
        return {
            "db_name": self.connection_conf.database,
            "db_host": self.connection_conf.db_host,
        }

    def cursor(self, **kwargs):
        connection = pyodbc.connect(
            driver="SQL Server",
            server=self._connection_details["db_host"],
            database=self._connection_details["db_name"],
            trusted_connection="Yes",
            **kwargs,
        )
        return connection.cursor()

    def engine(self, **kwargs):
        driver = "SQL+Server+Native+Client+11.0"
        return create_engine(
            (
                f"mssql+pyodbc://"
                f"{self._connection_details['db_host']}/"
                f"{self._connection_details['db_name']}?"
                f"driver={driver}"
            ),
            **kwargs,
        )

    def session_maker(self, engine=None, **kwargs):
        if engine:
            return sessionmaker(engine, **kwargs)
        else:
            return sessionmaker(self.engine(), **kwargs)

    def session(self):
        return Session(self.engine())

    def connection_check(self):
        cur = self.cursor()
        cur.execute("SELECT @@version")
        info = cur.fetchone()
        cur.close()
        print(
            f"\nConnection to {self.app} successful. \nDatabase info: \n\t{info[0].split(',')[0]}"
            ""
        )
