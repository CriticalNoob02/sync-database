def get_max_id_query(id_ref: str, table: str):
    return f"""SELECT
                    max({id_ref})
                FROM
                    {table}
;"""
