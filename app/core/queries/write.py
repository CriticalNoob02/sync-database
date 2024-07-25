def get_insert_query(columns: list[str], values: list[tuple], table: str) -> str:
    values_strings = [f"({', '.join(map(repr, value))})" for value in values]
    values_string = ",\n".join(values_strings)

    return (f"""
        INSERT INTO
            {table} ({', '.join(columns)})
        VALUES
            {values_string}
        ;""")
