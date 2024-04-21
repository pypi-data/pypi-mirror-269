from . import table20240326, table20240414, table20240419, table20240420


def get_table_factory(table_name):
    if table_name == "table20240326":
        return table20240326
    elif table_name == "table20240414":
        return table20240414
    elif table_name == "table20240419":
        return table20240419
    elif table_name == "table20240420":
        return table20240420
    else:
        raise NotImplementedError(f"Not supported <{table_name=}>.")
