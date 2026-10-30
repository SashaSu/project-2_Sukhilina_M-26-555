from prettytable import PrettyTable

from .utils import load_table_data


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


def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f"Таблицы {table_name} не существует")
        return None
    columns = metadata[table_name]
    column_names = list(columns.keys())
    if len(column_names) - 1 != len(values):
        print("Неверное количество значений")
        return None
    table_data = load_table_data(table_name)
    if table_data:
        new_id = max(record["ID"] for record in table_data) + 1
    else:
        new_id = 1
    new_record = {"ID": new_id}
    for index, column_name in enumerate(column_names):
        if column_name.upper() == "ID":
            continue
        cur_value = values[index - 1]
        column_type = columns[column_name]
        match column_type:
            case "int":
                if type(cur_value) is not int:
                    print(f"Столбец '{column_name}' должен иметь тип int")
                    return None
            case "str":
                if type(cur_value) is not str:
                    print(f"Столбец '{column_name}' должен иметь тип str")
                    return None
            case "bool":
                if type(cur_value) is not bool:
                    print(f"Столбец '{column_name}' должен иметь тип bool")
                    return None
        new_record[column_name] = cur_value
    table_data.append(new_record)
    return table_data


def select(table_name, where_clause=None):
    data = load_table_data(table_name)
    if where_clause is None:
        return data
    column_name = list(where_clause.keys())[0]
    value = list(where_clause.values())[0]
    result = []
    for record in data:
        if record[column_name] == value:
            result.append(record)
    return result


def drop_table(metadata, table_name):
    if table_name in metadata:
        del metadata[table_name]
    else:
        print("Таблица не существует")
    return metadata


def list_tables(metadata):
    for table_name in metadata:
        print(table_name)


def print_formatted_table(data):
    if not data:
        print("Пусто")
        return
    table = PrettyTable()
    table.field_names = list(data[0].keys())
    for record in data:
        table.add_row(list(record.values()))
    print(table)


def delete(table_data, where_clause):
    column_name = list(where_clause.keys())[0]
    value = list(where_clause.values())[0]
    if table_data and column_name not in table_data[0]:
        print(f"Столбца {column_name} не существует")
        return None
    result = []
    for record in table_data:
        if record[column_name] != value:
            result.append(record)
    return result


def info(metadata, table_name):
    if table_name not in metadata:
        print(f'Таблица "{table_name}" не существует')
        return
    columns = metadata[table_name]
    data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    column_info = []
    for column_name, column_type in columns.items():
        column_info.append(f"{column_name}:{column_type}")
    print(f"Столбцы: {', '.join(column_info)}")
    print(f"Количество записей: {len(data)}")


def update(table_data, set_clause, where_clause):
    set_column = list(set_clause.keys())[0]
    set_value = list(set_clause.values())[0]
    where_column = list(where_clause.keys())[0]
    where_value = list(where_clause.values())[0]
    for record in table_data:
        if record[where_column] == where_value:
            record[set_column] = set_value
    return table_data
