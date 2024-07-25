def get_reader_query_limit(id_ref: str, max_id: str, table: str, limit: int):
    return (f"""
           SELECT
                *
           FROM
                {table}
           WHERE
                {id_ref} > {max_id}
           ORDER BY
                {id_ref} ASC
           LIMIT
                {limit}
;""")


def get_reader_query(table: str):
    return (f"""
          SELECT
               *
          FROM
               {table}
""")
