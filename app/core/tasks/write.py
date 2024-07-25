from core.queries.write import get_insert_query
from core.tasks.connection import get_cursor_by_connection
from core.utils.rich_logs import get_traceback
from core.utils.rich_logs import LOG


def write(table_name: str, columns: list[str], connection, data: list[tuple]):
    try:
        final_cursor = get_cursor_by_connection(connection)
        query = get_insert_query(
            columns=columns,
            values=data,
            table=table_name
        )
        LOG.debug(query)
        final_cursor.execute(query)
    except Exception:
        get_traceback()
        exit(1)
