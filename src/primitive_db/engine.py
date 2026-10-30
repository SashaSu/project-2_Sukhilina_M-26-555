import prompt

from .core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    list_tables,
    print_formatted_table,
    select,
    update,
)
from .parser import (
    parse_create_table,
    parse_delete,
    parse_drop_table,
    parse_info,
    parse_insert,
    parse_select,
    parse_simple_command,
    parse_update,
)
from .utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "
          "- создать запись")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - "
          "прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print(
        "<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where "
        "<столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> where <столбец> = "
          "<значение> - удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    print("***База данных***")
    print_help()
    filepath = "db_meta.json"
    metadata = load_metadata(filepath)
    while True:
        command = prompt.string("Введите команду: ")
        if not command:
            continue
        parsed_command = command.strip().split()[0]
        try:
            match parsed_command:
                case "exit":
                    parse_simple_command(command, "exit")
                    break
                case "help":
                    parse_simple_command(command, "help")
                    print_help()
                case "list_tables":
                    parse_simple_command(command, "list_tables")
                    list_tables(metadata)
                case "create_table":
                    table_name, columns = parse_create_table(command)
                    if create_table(metadata, table_name, columns) is not None:
                        save_metadata(filepath, metadata)
                case "insert":
                    table_name, values = parse_insert(command)
                    data = insert(metadata, table_name, values)
                    if data is not None:
                        save_table_data(table_name, data)
                case "drop_table":
                    table_name = parse_drop_table(command)
                    if drop_table(metadata, table_name) is not None:
                        save_metadata(filepath, metadata)
                case "select":
                    table_name, where_clause = parse_select(command)
                    if table_name not in metadata:
                        print(f'Таблица "{table_name}" не существует')
                        continue
                    data = select(table_name, where_clause)
                    print_formatted_table(data)
                case "delete":
                    table_name, where_clause = parse_delete(command)
                    if table_name not in metadata:
                        print(f'Таблица "{table_name}" не существует')
                        continue
                    data = load_table_data(table_name)
                    new_data = delete(data, where_clause)
                    if len(new_data) == len(data):
                        print("Нет таких записей")
                    else:
                        save_table_data(table_name, new_data)
                case "info":
                    table_name = parse_info(command)
                    info(metadata, table_name)
                case "update":
                    table_name, set_clause, where_clause = parse_update(command)
                    if table_name not in metadata:
                        print(f'Таблица "{table_name}" не существует')
                        continue
                    data = load_table_data(table_name)
                    new_data = update(data, set_clause, where_clause)
                    save_table_data(table_name, new_data)
                case _:
                    print("Неизвестная команда")

        except ValueError as error:
            print(error)
