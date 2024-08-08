def get_truncate_query(table, schema):
    return f"TRUNCATE {schema}.{table}"
