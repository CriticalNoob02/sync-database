from prometheus_client import Counter, Gauge

RUNNING = Gauge('service_running', 'Indica que o servico está rodando')
ATT_TABLE = Gauge('table_is_updated', 'Indica que a tabela foi atualizada', ['table'])
TIME_COUNT = Counter('time_count', 'Tempo para finalizar uma tabela', ['table'])
