def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f"Таблица '{table_name}' уже существует")
        return None
    allowed_types = ["int", "str", "bool"]
    table_columns = {"ID": "int"}
    for column in columns:
        args = column.split(":")
        if len(args) != 2:
            print("Неверное количество аргументов")
            return None
        column_name, column_type = args
        if column_type not in allowed_types or not column_name:
            print(f"Неверный тип столбца '{column}'")
            return None
        if column_name.upper() != "ID":
            table_columns[column_name] = column_type
    metadata[table_name] = table_columns
    return metadata


def drop_table(metadata, table_name):
    if table_name in metadata:
        del metadata[table_name]
    else:
        print("Таблица не существует")
    return metadata


def list_tables(metadata):
    for table_name in metadata:
        print(table_name)
