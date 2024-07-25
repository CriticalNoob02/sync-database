def not_null_execute(cursor, query: str):
    cursor.execute(query)
    result = cursor.fetchone()

    if result[0] is None:
        return 0
    else:
        return result[0]
