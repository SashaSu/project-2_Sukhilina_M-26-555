from prettytable import PrettyTable

from .decorators import confirm_action, create_cacher, handle_db_errors, log_time
from .utils import load_table_data
cache_result, clear_cache = create_cacher()


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает таблицу"""
    if table_name in metadata:
        raise ValueError(f"Таблица '{table_name}' уже существует")
    allowed_types = ["int", "str", "bool"]
    table_columns = {"ID": "int"}
    for column in columns:
        args = column.split(":")
        if len(args) != 2:
            raise ValueError("Неверный формат описания столбца")
        column_name, column_type = args
        if column_type not in allowed_types or not column_name:
            raise ValueError(f"Неверный тип или имя столбца '{column}'")
        if column_name.upper() != "ID":
            table_columns[column_name] = column_type
    metadata[table_name] = table_columns
    clear_cache()
    return metadata


@log_time
@handle_db_errors
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу"""
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не существует")
    columns = metadata[table_name]
    column_names = list(columns.keys())
    if len(column_names) - 1 != len(values):
        raise ValueError("Неверное количество значений")
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
                    raise ValueError(f"Столбец '{column_name}' должен иметь тип int")
            case "str":
                if type(cur_value) is not str:
                    raise ValueError(f"Столбец '{column_name}' должен иметь тип str")
            case "bool":
                if type(cur_value) is not bool:
                    raise ValueError(f"Столбец '{column_name}' должен иметь тип bool")
        new_record[column_name] = cur_value
    table_data.append(new_record)
    clear_cache()
    return table_data


@log_time
@handle_db_errors
def select(table_name, where_clause=None):
    """Возвращает записи таблицы с учетом условия"""
    def get_data():
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
    if where_clause is None:
        key = (table_name, None)
    else:
        key = (table_name, str(where_clause))
    return cache_result(key, get_data)


@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу"""
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не существует")
    del metadata[table_name]
    with open(f"data/{table_name}.json", "w", encoding="utf-8") as f:
        f.write("[]")
    clear_cache()
    return metadata


def list_tables(metadata):
    """Выводит список таблиц"""
    for table_name in metadata:
        print(table_name)


def print_formatted_table(data):
    """Выводит записи в виде таблицы"""
    if not data:
        print("Пусто")
        return
    table = PrettyTable()
    table.field_names = list(data[0].keys())
    for record in data:
        table.add_row(list(record.values()))
    print(table)


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Удаляет записи, соответствующие условию"""
    column_name = list(where_clause.keys())[0]
    value = list(where_clause.values())[0]
    if table_data and column_name not in table_data[0]:
        raise KeyError(f"Столбец '{column_name}' не существует")
    result = []
    for record in table_data:
        if record[column_name] != value:
            result.append(record)
    clear_cache()
    return result


@handle_db_errors
def info(metadata, table_name):
    """Выводит информацию о структуре таблицы"""
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует')
    columns = metadata[table_name]
    data = load_table_data(table_name)
    print(f"Таблица: {table_name}")
    column_info = []
    for column_name, column_type in columns.items():
        column_info.append(f"{column_name}:{column_type}")
    print(f"Столбцы: {', '.join(column_info)}")
    print(f"Количество записей: {len(data)}")


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Изменяет значения столбцов в записях"""
    set_column = list(set_clause.keys())[0]
    set_value = list(set_clause.values())[0]
    where_column = list(where_clause.keys())[0]
    where_value = list(where_clause.values())[0]
    for record in table_data:
        if record[where_column] == where_value:
            record[set_column] = set_value
    clear_cache()
    return table_data