from core.tasks import read, write, mapping, truncate
from core.config.envs import get_query_limit
from core.utils.rich_logs import get_traceback
from core.utils.monitoring import ATT_TABLE
import importlib
import logging
import os


def sync_truncate(table,
                  SOURCE,
                  SOURCE_PATH,
                  source_conn,
                  final_conn,
                  source_module,
                  final_module) -> None:

    HAVE_PROCESS = os.path.exists(f'{SOURCE_PATH}/{table}/process.py')
    HAVE_DECIDER = os.path.exists(f'{SOURCE_PATH}/{table}/decider.py')
    BATCH_SIZE = source_module.table_map["limit"] or get_query_limit()

    try:
        DECIDER = True
        if HAVE_DECIDER:
            decider = importlib.import_module(f'modules.{SOURCE}.tables.{table}.decider')
            DECIDER = decider.decider(source_conn)

        if DECIDER:
            truncate(
                final_conn=final_conn,
                table=final_module.table_map["table"],
                schema=final_module.table_map["schema"]
                )

            result_cursor = read(
                source_conn=source_conn,
                final_conn=final_conn,
                source_table=source_module.table_map["table"],
                final_table=final_module.table_map["table"],
                source_ref=False,
                final_ref=False
                )

            if not result_cursor:
                return None

        else:
            logging.debug('Tabela ja esta atualizada...')
            return None

        logging.debug(f'batch size: {BATCH_SIZE}')
        while True:
            logging.debug('running again...')
            rows = result_cursor.fetchmany(size=BATCH_SIZE)
            if not rows:
                break

            if HAVE_PROCESS:
                process = importlib.import_module(f'modules.{SOURCE}.tables.{table}.process')
                rows = process.process(rows)

            columns = mapping(
                conn=final_conn,
                table=final_module.table_map["table"],
                schema=final_module.table_map["schema"]
                )

            write(
                table_name=final_module.table_map["table"],
                columns=columns,
                connection=final_conn,
                data=rows
                )

            ATT_TABLE.labels(table=table).set(1)

    except Exception:
        get_traceback()
