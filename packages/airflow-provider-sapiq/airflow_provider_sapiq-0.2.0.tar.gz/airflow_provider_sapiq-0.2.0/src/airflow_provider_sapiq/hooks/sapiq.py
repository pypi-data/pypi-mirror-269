"""SAP IQ hook module."""

from __future__ import annotations
from typing import TYPE_CHECKING
import time

import sqlanydb

from airflow.providers.common.sql.hooks.sql import DbApiHook

if TYPE_CHECKING:
    from typing import Any


class SapIQHook(DbApiHook):
    """Interact with SAP IQ."""

    DEFAULT_SQLALCHEMY_SCHEME = "sqlalchemy_sqlany"
    conn_name_attr = "sapiq_conn_id"
    default_conn_name = "sapiq_default"
    conn_type = "sapiq"
    hook_name = "SAP IQ"
    supports_autocommit = True
    placeholder = "?"
    __default_port = 2638

    @classmethod
    def get_connection_form_widgets(cls) -> dict[str, Any]:
        """Return connection widgets to add to connection form."""
        from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import StringField

        return {
            "appinfo": StringField(
                lazy_gettext("AppInfo"), widget=BS3TextFieldWidget()
            ),
            "retries": StringField(
                lazy_gettext("Retries"), widget=BS3TextFieldWidget()
            ),
            "retry_delay": StringField(
                lazy_gettext("Retry Delay"), widget=BS3TextFieldWidget()
            ),
        }

    @classmethod
    def get_ui_field_behaviour(cls):
        """Returns custom field behaviour"""
        return {
            "hidden_fields": ["extra", "schema"],
            "relabeling": {
                "login": "User Id",
                "appinfo": "AppInfo",
                "retries": "Retries",
                "retry_delay": "Retry Delay",
            },
            "placeholders": {
                "host": "host",
                "port": "2638",
                "login": "guest",
                "password": "guest",
                "appinfo": "",
                "retries": "1",
                "retry_delay": "60",
            },
        }

    def __init__(
        self,
        *args,
        conn_id: str | None = None,
        appinfo: str | None = None,
        log_sql: bool = True,
        **kwargs,
    ):
        if conn_id:
            kwargs[self.conn_name_attr] = conn_id
        super().__init__(log_sql=log_sql, *args, **kwargs)
        self._appinfo = appinfo
        self._placeholder: str = "?"

    def get_conn(
        self,
        appinfo: str | None = None,
        retries: int | None = None,
        retry_delay: int | None = None,
    ) -> sqlanydb.Connection:
        """Return sap iq connection object"""
        connection = self.get_connection(getattr(self, self.conn_name_attr))
        params = {
            "userid": connection.login,
            "password": connection.password or "",
        }
        appinfo_ = " ".join(
            filter(
                None, [connection.extra_dejson.get("appinfo"), self._appinfo, appinfo]
            )
        )
        if appinfo_:
            params["appinfo"] = appinfo_
        connection_port = connection.port or SapIQHook.__default_port
        # Split the string by comma to get individual host:port pairs
        host_port_pairs = connection.host.split(",")
        hosts_list = []
        for pair in host_port_pairs:
            # Split the pair by colon to separate host and port
            parts = pair.split(":")
            host = parts[0] or "localhost"
            port = int(parts[1]) if len(parts) > 1 else connection_port
            hosts_list.append(f"{host}:{port}")
        retries_ = retries or int(connection.extra_dejson.get("retries", 1))
        if retries_ < 1:
            retries_ = 1
        retry_delay_ = retry_delay or int(
            connection.extra_dejson.get("retry_delay", 60)
        )
        err: BaseException | None = None
        conn = None
        while retries_:
            retries_ -= 1
            for host in hosts_list:
                try:
                    err = None
                    self.log.info("Connecting to host: %s", host)
                    conn = sqlanydb.connect(**params, host=host)
                    retries_ = 0
                    break
                except sqlanydb.OperationalError as ex:
                    self.log.error(ex)
                    err = ex
            if retries_:
                self.log.info("Retry after %s sec", retry_delay_)
                time.sleep(retry_delay_)
        if err:
            raise err
        return conn

    def get_uri(self) -> str:
        """URI invoked in :py:meth:`~airflow.hooks.dbapi.DbApiHook.get_sqlalchemy_engine` method.

        Extract the URI from the connection.

        :return: the extracted uri.
        """
        from urllib.parse import quote_plus, urlunsplit

        conn = self.get_connection(getattr(self, self.conn_name_attr))
        login = ""
        if conn.login:
            login = f"{quote_plus(conn.login)}:{quote_plus(conn.password)}@"
        host = conn.host
        if conn.port is not None:
            host += f":{conn.port}"
        schema = conn.schema or ""
        uri = urlunsplit(
            (self.DEFAULT_SQLALCHEMY_SCHEME, f"{login}{host}", schema, "", "")
        )
        return uri
