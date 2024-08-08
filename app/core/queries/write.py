def get_insert_query(columns: list[str], values: list[tuple], table: str) -> str:
    def sql_repr(value):
        if value is None:
            return 'NULL'
        return repr(value)

    values_strings = [f"({', '.join(map(sql_repr, value))})" for value in values]
    values_string = ",\n".join(values_strings)

    return f"""
        INSERT INTO
            {table} ({', '.join(columns)})
        VALUES
            {values_string}
        ;"""
