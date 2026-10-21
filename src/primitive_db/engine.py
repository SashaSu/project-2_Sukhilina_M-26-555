import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

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
        try:
            parsed_command = shlex.split(command)
        except ValueError:
            print("Некорректная команда.")
            continue
        actual_command = parsed_command[0]
        args = parsed_command[1:]
        if actual_command in ["exit", "help", "list_tables"] and len(args) > 0:
            print("Некорректная команда.")

        match actual_command:
            case "exit":
                break
            case "help":
                print_help()
            case "list_tables":
                list_tables(metadata)
                pass
            case "create_table":
                if len(args) < 1:
                    print("Неверное число аргументов")
                    continue
                if create_table(metadata, args[0], args[1:]) is not None:
                    save_metadata(filepath, metadata)
                pass
            case "drop_table":
                if len(args) > 1:
                    print("Неверное число аргументов")
                    continue
                if drop_table(metadata, args[0]) is not None:
                    save_metadata(filepath, metadata)
            case _:
                print("Неизвестная команда")
