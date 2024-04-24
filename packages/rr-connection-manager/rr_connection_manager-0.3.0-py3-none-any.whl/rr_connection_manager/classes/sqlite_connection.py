# SQLite is currently not supported

from .connection import Connection


class SQLiteConnection(Connection):
    def __init__(self, app=None, tunnel=None) -> None:
        super().__init__(app, tunnel)
        self._connection_details = self._set_details()

    def _set_details(self):
        pass

    def cursor(self, **kwargs):
        pass

    def engine(self, **kwargs):
        pass

    def session_maker(self, **kwargs):
        pass

    def session(self):
        pass

    def connection_check(self):
        pass
