from core.config.envs import get_module_final, get_module_source, get_query_limit
from prometheus_client import start_http_server, Counter, Gauge
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

# Metrics
RUNNING = Gauge('service_running', 'Indica que o saervico está rodando')
READ_COUNT = Counter('read_count', 'Numero de linhas lidas', ['table'])
WRITE_COUNT = Counter('write_count', 'Numero de linhas que serão escritas', ['table'])
TIME_COUNT = Counter('time_count', 'Tempo para finalizar uma tabela', ['table'])
start_http_server(8000)

RUNNING.set(1)

for index, table in enumerate(sorted(os.listdir(SOURCE_PATH))):
    start = time.perf_counter()

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
            final_module=final_module,
            READ_COUNT=READ_COUNT,
            WRITE_COUNT=WRITE_COUNT
        )
    else:
        sync_truncate(
            table=table,
            SOURCE=SOURCE,
            SOURCE_PATH=SOURCE_PATH,
            source_conn=source_conn,
            final_conn=final_conn,
            source_module=source_module,
            final_module=final_module,
            READ_COUNT=READ_COUNT,
            WRITE_COUNT=WRITE_COUNT
        )

    end = time.perf_counter()
    TIME_COUNT.labels(table=table).inc(end-start)
    logging.info(f"Concluindo tasks - {table}")

# time.sleep(25)
RUNNING.set(0)
