from core.config.envs import get_db_driver


def get_mapper_table(table: str, schema: str):
    match get_db_driver():
        case "postgres":
            return f"""
            SELECT
                column_name, column_default
            FROM
                information_schema.columns
            WHERE
                table_schema = '{schema}' AND table_name = '{table}'
            ;"""
        case "oracle":
            return """Futuramente..."""
