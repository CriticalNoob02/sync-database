from core.queries.mapper_table import get_mapper_table
from core.tasks.connection import get_cursor_by_connection
import logging


def mapping(conn, table: str, schema: str):
    cursor = get_cursor_by_connection(conn)
    query = get_mapper_table(
        table=table,
        schema=schema
        )
    cursor.execute(query)
    result = cursor.fetchall()

    result = [col[0] for col in result if not (col[1] and 'nextval' in col[1])]

    logging.debug(f"Colunas mapeamento: {result}")
    return result
