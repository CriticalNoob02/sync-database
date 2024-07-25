from core.config.drive.postgresql import connect_ps
from core.config.drive.oracle import connect_oracle
from core.utils.rich_logs import get_traceback
from core.config.envs import get_db_driver

DRIVER = get_db_driver()


def get_connections(isSource: bool):
    try:
        match DRIVER:
            case "oracle":
                conn = connect_oracle(isSource)
                return conn
            case "postgres":
                conn = connect_ps(isSource)
                conn.set_session(autocommit=True)
                return conn
            case _:
                return False
    except Exception:
        get_traceback()
        exit(1)


def get_cursor_by_connection(conn):
    match DRIVER:
        case "postgres":
            return conn.cursor()
        case "oracle":
            return conn.cursor()
