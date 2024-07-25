from core.queries.mapper_table import get_mapper_table
from core.tasks.connection import get_cursor_by_connection


def mapping(conn, table: str, schema: str, pk_ref: str = False):
    cursor = get_cursor_by_connection(conn)
    query = get_mapper_table(
        table=table,
        schema=schema
        )
    cursor.execute(query)
    result = cursor.fetchall()
    col_list = [item for tupla in result for item in tupla]
    if pk_ref:
        col_list.remove(pk_ref)
    return col_list
