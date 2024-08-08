from core.utils.rich_logs import get_traceback


def process(list_reader: list[tuple]):
    list_writer = []
    try:
        for row in list_reader:
            id_origem = row[0]
            name = str(row[1])

            list_writer.append((
                id_origem,
                name
                ))

        return list_writer
    except Exception:
        get_traceback()
        return False
