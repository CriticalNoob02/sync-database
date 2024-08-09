from core.config.envs import get_module_final, get_module_source, get_query_limit
from prometheus_client import start_http_server
from core.utils.monitoring import RUNNING, TIME_COUNT, ATT_TABLE
from core.tasks import get_connections
from sync_ref import sync_ref
from sync_truncate import sync_truncate
from dotenv import load_dotenv
import importlib
import os
import time
import logging

load_dotenv("./infra/envs/.env")

# Variables;
SOURCE = get_module_source()
FINAL = get_module_final()
LIMIT = get_query_limit()
SOURCE_PATH = f"./app/modules/{SOURCE}/tables"
FINAL_PATH = f"./app/modules/{FINAL}/tables"
source_conn = get_connections(isSource=True)
final_conn = get_connections(isSource=False)

start_http_server(8000)
RUNNING.set(1)

for index, table in enumerate(sorted(os.listdir(SOURCE_PATH))):
    ATT_TABLE.labels(table=table).set(0)
    time_start = time.time()

    source_module = importlib.import_module(f'modules.{SOURCE}.tables.{table}.mapper')
    final_module = importlib.import_module(f'modules.{FINAL}.tables.{sorted(os.listdir(FINAL_PATH))[index]}.mapper')
    HAVE_REF = source_module.table_map['ref']

    logging.info(f"Iniciando tasks - {table}")

    if HAVE_REF:
        sync_ref(
            table=table,
            SOURCE=SOURCE,
            SOURCE_PATH=SOURCE_PATH,
            source_conn=source_conn,
            final_conn=final_conn,
            source_module=source_module,
            final_module=final_module
        )
    else:
        sync_truncate(
            table=table,
            SOURCE=SOURCE,
            SOURCE_PATH=SOURCE_PATH,
            source_conn=source_conn,
            final_conn=final_conn,
            source_module=source_module,
            final_module=final_module
        )

    logging.info(f"Concluindo tasks - {table}")
    TIME_COUNT.labels(table=table).inc(time.time() - time_start)

time.sleep(20)
RUNNING.set(0)
