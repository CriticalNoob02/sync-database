def get_reader_query_ref(id_ref: str, max_id: str, table: str):
    return (f"""
           SELECT
                *
           FROM
                {table}
           WHERE
                {id_ref} > {max_id}
;""")


def get_reader_query(table: str):
    return (f"""
          SELECT
               *
          FROM
               {table}
""")
