from core.tasks.connection import get_cursor_by_connection
from core.queries.max_id import get_max_id_query
from core.queries.reader import get_reader_query_ref, get_reader_query
from core.utils.rich_logs import get_traceback
from core.utils.db_functions import not_null_execute
from psycopg2.extensions import cursor
from typing import Literal, Optional
import logging


def read(source_conn,
         final_conn,
         source_table: str,
         final_table: str,
         source_ref: str | Literal[False],
         final_ref: str | Literal[False]
         ) -> Optional[cursor]:

    source_cursor = get_cursor_by_connection(source_conn)
    final_cursor = get_cursor_by_connection(final_conn)

    try:
        # not have ref
        if not source_ref:
            query = get_reader_query(
                table=source_table
                )
            source_cursor.execute(query)
            return source_cursor

        # have ref
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
            logging.debug(f"Tabela já atualizada | id final: {max_id_final}")
            return None

        else:
            query = get_reader_query_ref(
                id_ref=source_ref,
                max_id=max_id_final,
                table=source_table
                )
            source_cursor.execute(query)
            return source_cursor

    except Exception:
        get_traceback()
        exit(1)
