from sshtunnel import SSHTunnelForwarder

from .connection_conf import ConnectionConf


class Connection:
    def __init__(self, app=None, tunnel=None, via_app=None) -> None:
        self.app = app
        self.connection_conf = ConnectionConf(app, via_app)
        self.tunnel = self._create_tunnel(tunnel)

    def _create_tunnel(self, tunnel):
        # If not going via an app server tunnel is direct to DB so DB is local
        if tunnel:
            ssh_port = int(self.connection_conf.tunnel_port)
            db_port = int(self.connection_conf.db_port)
            db_host = self.connection_conf.db_host
            ssh_address_or_host = (db_host, ssh_port)
            remote_bind_address = ("localhost", db_port)
            # If going via an app server then DB is remote so bind using DB address
            if self.connection_conf.via_app_server:
                app_host = self.connection_conf.app_host
                ssh_address_or_host = (app_host, ssh_port)
                remote_bind_address = (db_host, db_port)

            return SSHTunnelForwarder(
                ssh_address_or_host=ssh_address_or_host,
                ssh_username=self.connection_conf.tunnel_user,
                ssh_pkey="~/.ssh/id_rsa",
                remote_bind_address=remote_bind_address,
            )
        # If no tunnel then running on DB server so no tunnel
        # This is wrong if running on an app server. Needs testing
        return None

    def close(self):
        if self.tunnel:
            self.tunnel.stop()
