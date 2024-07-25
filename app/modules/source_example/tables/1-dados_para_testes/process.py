from core.utils.rich_logs import get_traceback


def process(list_reader: list[tuple]):
    list_writer = []
    try:
        for index, row in enumerate(list_reader):
            natural_id = str(row[0])
            text_import = str(row[1])
            number_import = str(row[2])
            list_writer.append((natural_id, text_import, number_import))
        return list_writer
    except Exception:
        get_traceback()
        return False
