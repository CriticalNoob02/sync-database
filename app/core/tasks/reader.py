from core.tasks.connection import get_cursor_by_connection
from core.queries.max_id import get_max_id_query
from core.queries.reader import get_reader_query, get_reader_query_limit
from core.utils.rich_logs import LOG, get_traceback
from core.utils.db_functions import not_null_execute


def read(source_conn,
         final_conn,
         source_table: str,
         final_table: str,
         source_ref: str | bool,
         final_ref: str | bool,
         limit: int,) -> list:

    source_cursor = get_cursor_by_connection(source_conn)
    final_cursor = get_cursor_by_connection(final_conn)

    try:
        # no limit
        if not source_ref:
            query = get_reader_query(
                    table=source_table
                    )
            source_cursor.execute(query)
            return source_cursor.fetchall()

        # have limit
        query = get_max_id_query(
            id_ref=source_ref,
            table=source_table
            )
        max_id_source = not_null_execute(source_cursor, query)
        query = get_max_id_query(
            id_ref=final_ref,
            table=final_table
            )
        max_id_final = not_null_execute(final_cursor, query)

        if max_id_source == max_id_final:
            LOG.info(f"Tabela já atualizada | id final: {max_id_final}")
            return []

        else:
            query = get_reader_query_limit(
                id_ref=source_ref,
                max_id=max_id_final,
                table=source_table,
                limit=limit
                )
            source_cursor.execute(query)
            return source_cursor.fetchall()

    except Exception:
        get_traceback()
        exit(1)
