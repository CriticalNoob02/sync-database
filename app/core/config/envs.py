import os


def get_query_limit() -> int:
    return 5


def get_module_source() -> str:
    return os.environ.get('MODULE_SOURCE', 'teste_source')


def get_module_final() -> str:
    return os.environ.get('MODULE_FINAL', 'teste_final')


def get_db_driver() -> str:
    return os.environ.get('DB_DRIVER', 'postgres')
