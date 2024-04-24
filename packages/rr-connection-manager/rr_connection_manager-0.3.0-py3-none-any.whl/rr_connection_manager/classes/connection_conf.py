import hashlib
import json
import os
import getpass

from dotenv import dotenv_values
from pykeepass import PyKeePass


class ConnectionConf:
    def __init__(self, app, via_app) -> None:
        self.app = app
        self.conf = dotenv_values(".connection_env")
        self.via_app_server = via_app
        self.app_host = None
        self.db_host = None
        self.db_user = None
        self.database = None
        self.db_password = None
        self.tunnel_user = None
        self.db_port = None
        self.tunnel_port = None
        self._set_attributes()

    def _get_keepass_key(self):
        with open(
            os.path.expanduser("~/.ssh/id_rsa.pub"), "r", encoding="utf-8"
        ) as public_key_file:
            public_key = public_key_file.read()

        sha256_hash = hashlib.sha256()
        sha256_hash.update(public_key.encode("utf-8"))

        return sha256_hash.hexdigest()

    def _set_attributes(self):
        if len(self.conf) > 0:
            if "APP_HOST" in self.conf:
                self.app_host = self.conf["APP_HOST"]
            if "DB_HOST" in self.conf:
                self.db_host = self.conf["DB_HOST"]
            else:
                # This might not be the case for SQLite
                raise ValueError(
                    "DB_HOST is a required variable if you are using a .connection_env file"
                )
            if "DB_USER" in self.conf:
                self.db_user = self.conf["DB_USER"]
            if "DATABASE" in self.conf:
                self.database = self.conf["DATABASE"]
            else:
                # This might not be the case for SQLite
                raise ValueError(
                    "DATABASE is a variable if you are using a .connection_env file"
                )
            if "DB_PASSWORD" in self.conf:
                self.db_password = self.conf["DB_PASSWORD"]
            if "TUNNEL_USER" in self.conf:
                self.tunnel_user = self.conf["TUNNEL_USER"]
            if "DB_PORT" in self.conf:
                self.db_port = self.conf["DB_PORT"]
            if "TUNNEL_PORT" in self.conf:
                self.tunnel_port = self.conf["TUNNEL_PORT"]

        else:
            user = getpass.getuser().replace(".", "_")
            keepass_file_path = os.path.abspath(
                os.path.join("R:", "Connection Manager", user, f"{user}.kdbx ")
            )

            if not os.path.exists(keepass_file_path):
                raise FileExistsError(
                    "Can't find your keepass file. You might need to run rr-key-manager"
                )

            kp = PyKeePass(
                keepass_file_path,
                password=self._get_keepass_key(),
            )

            group = kp.find_groups(name=self.app, first=True)

            if any(e for e in group.entries if "db_server" in e.path):
                db_server = next((e for e in group.entries if "db_server" in e.path))
                self.db_host = db_server.url
                self.tunnel_user = db_server.username

                if db_server.notes and "PORTS" in db_server.notes:
                    self.db_port = json.loads(db_server.notes)["PORTS"]["DB_PORT"]
                    self.tunnel_port = json.loads(db_server.notes)["PORTS"]["SSH_PORT"]

            if any(e for e in group.entries if "db_user" in e.path):
                db_user = next((e for e in group.entries if "db_user" in e.path))
                self.db_user = db_user.username
                self.db_password = db_user.password

                if db_user.notes and "DATABASE" in db_user.notes:
                    self.database = json.loads(db_user.notes)["DATABASE"][0]

            if any(e for e in group.entries if "app_server" in e.path):
                app_server = next((e for e in group.entries if "app_server" in e.path))
                self.app_host = app_server.url

                if (
                    self.via_app_server == "true"
                    and app_server.notes
                    and "PORTS" in app_server.notes
                ):
                    self.tunnel_user = app_server.username
                    self.tunnel_port = json.loads(app_server.notes)["PORTS"]["SSH_PORT"]
