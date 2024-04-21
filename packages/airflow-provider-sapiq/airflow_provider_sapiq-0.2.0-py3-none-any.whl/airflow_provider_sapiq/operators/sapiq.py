from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Mapping, Optional, Sequence, Union

from airflow.models import BaseOperator
from airflow.exceptions import AirflowException
from airflow_provider_sapiq.hooks.sapiq import SapIQHook
import textwrap

if TYPE_CHECKING:
    from airflow.providers.common.sql.hooks.sql import DbApiHook
    from airflow.utils.context import Context


class SapIqOperator(BaseOperator):
    """
    Executes sql code in a specific SAP IQ database

    This operator may use one of two hooks, depending on the ``conn_type`` of the connection.

    If conn_type is ``'odbc'``, then :py:class:`~airflow.providers.odbc.hooks.odbc.OdbcHook`
    is used.  Otherwise, :py:class:`~airflow.providers.microsoft.mssql.hooks.mssql.MsSqlHook` is used.

    :param sql: the sql code to be executed (templated)
    :param sapiq_conn_id: reference to a specific mssql database
    :param parameters: (optional) the parameters to render the SQL query with.
    :param autocommit: if True, each command is automatically committed.
        (default value: False)
    """
    template_fields: Sequence[str] = ('sql', 'parameters', 'sapiq_conn_id')
    template_ext: Sequence[str] = ('.sql', )

    ui_color = '#00b9f2'

    def __init__(
        self,
        *,
        sql: str,
        sapiq_conn_id: str = 'sapiq_default',
        parameters: Optional[Union[Mapping, Iterable]] = None,
        autocommit: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.sapiq_conn_id = sapiq_conn_id
        self.sql = sql
        self.parameters = parameters
        self.autocommit = autocommit
        self._hook: Optional[Union[SapIQHook, 'DbApiHook']] = None

    def get_hook(self) -> Optional[Union[SapIQHook, 'DbApiHook']]:
        """
        Will retrieve hook as determined by :meth:`~.Connection.get_hook` if one is defined, and
        :class:`~.SapIQHook` otherwise.

        For example, if the connection ``conn_type`` is ``'odbc'``, :class:`~.OdbcHook` will be used.
        """
        if not self._hook:
            conn = SapIQHook.get_connection(conn_id=self.sapiq_conn_id)
            conn.conn_type = 'sapiq'
            try:
                self._hook = conn.get_hook()
            except AirflowException:
                self._hook = SapIQHook(sapiq_conn_id=self.sapiq_conn_id)
        return self._hook

    def execute(self, context: 'Context') -> None:
        sql = textwrap.dedent(self.sql).strip()
        self.log.info('Executing: %s', sql)
        hook = self.get_hook()
        hook.run(  # type: ignore[union-attr]
            sql=sql,
            autocommit=self.autocommit,
            parameters=self.parameters)
