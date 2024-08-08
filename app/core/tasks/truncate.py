from core.tasks.connection import get_cursor_by_connection
from core.queries.truncate import get_truncate_query
from core.utils.rich_logs import get_traceback


def truncate(final_conn, table: str, schema: str):
    try:
        final_cursor = get_cursor_by_connection(final_conn)
        query = get_truncate_query(table, schema)
        final_cursor.execute(query)
    except Exception:
        get_traceback()
        exit(1)
