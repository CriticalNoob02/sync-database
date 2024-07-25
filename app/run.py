from core.config.envs import get_module_final, get_module_source, get_query_limit
from prometheus_client import start_http_server, Counter, Gauge
from core.tasks import get_connections, read, write, mapping
from core.utils.rich_logs import LOG
from dotenv import load_dotenv
import importlib
import os
import time

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

for index, table in enumerate(reversed(os.listdir(SOURCE_PATH))):
    source_module = importlib.import_module(f'modules.{SOURCE}.tables.{table}.mapper')
    final_module = importlib.import_module(f'modules.{FINAL}.tables.{os.listdir(FINAL_PATH)[index]}.mapper')

    HAVE_REF = source_module.table_map["ref"] or False
    HAVE_PROCESS = os.path.exists(f'{SOURCE_PATH}/{table}/process.py') or False

    LOG.info(f"Iniciando tasks - {table}")
    start = time.perf_counter()
    list_reader = read(
        source_conn=source_conn,
        final_conn=final_conn,
        source_table=source_module.table_map["table"],
        final_table=final_module.table_map["table"],
        source_ref=HAVE_REF,
        final_ref=final_module.table_map["ref"] or False,
        limit=source_module.table_map["limit"],
        )

    READ_COUNT.labels(table=table).inc(len(list_reader))

    if list_reader:
        if HAVE_PROCESS:
            process = importlib.import_module(f'modules.{SOURCE}.tables.{table}.process')
            list_reader = process.process(list_reader)
            if not list_reader:
                continue

        columns = mapping(
            conn=final_conn,
            table=final_module.table_map["table"],
            schema=final_module.table_map["schema"],
            pk_ref=final_module.table_map["ref"] or False,
            )

        write(
            table_name=final_module.table_map["table"],
            columns=columns,
            connection=final_conn,
            data=list_reader
            )

    end = time.perf_counter()

    TIME_COUNT.labels(table=table).inc(end-start)
    WRITE_COUNT.labels(table=table).inc(len(list_reader))
    LOG.info(f"Concluindo tasks - {table}")

time.sleep(25)
RUNNING.set(0)
