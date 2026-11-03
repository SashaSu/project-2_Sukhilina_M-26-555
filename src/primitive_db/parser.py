import shlex


def parse_simple_command(command, real_command):
    """Проверяет корректность простой команды"""
    parts = shlex.split(command)
    if len(parts) != 1 or parts[0] != real_command:
        raise ValueError("Неверное число аргументов")
    return True


def parse_create_table(command):
    """Проверяет корректность создания таблицы"""
    parts = shlex.split(command)
    if len(parts) < 3 or parts[0] != "create_table":
        raise ValueError("Неверное число аргументов")
    table_name = parts[1]
    columns = parts[2:]
    return table_name, columns


def parse_drop_table(command):
    """Проверяет корректность удаления таблицы"""
    parts = shlex.split(command)
    if len(parts) != 2 or parts[0] != "drop_table":
        raise ValueError("Неверное число аргументов")
    return parts[1]


def parse_insert(command):
    """Проверяет корректность вставки таблицы"""
    parts = command.split("values")
    if len(parts) != 2:
        raise ValueError("Неверная команда")
    command_parts = parts[0].split()
    if (len(command_parts) != 3 or command_parts[0] != "insert"
            or command_parts[1] != "into"):
        raise ValueError("Неверная команда")
    table_name = command_parts[2]
    raw_values = parts[1].strip()
    if not raw_values.startswith("(") or not raw_values.endswith(")"):
        raise ValueError("Неверная команда")
    raw_values = raw_values[1:-1]
    items = []
    current = ""
    is_in_quotes = False
    for char in raw_values:
        if char == '"':
            is_in_quotes = not is_in_quotes
            current += char
        elif char == "," and not is_in_quotes:
            items.append(current.strip())
            current = ""
        else:
            current += char
    if is_in_quotes:
        raise ValueError("Незакрытые кавычки")
    items.append(current.strip())
    parsed_values = []
    for item in items:
        if item.startswith('"') and item.endswith('"'):
            parsed_value = item[1:-1]
        elif item.lower() == "true":
            parsed_value = True
        elif item.lower() == "false":
            parsed_value = False
        else:
            parsed_value = int(item)
        parsed_values.append(parsed_value)
    return table_name, parsed_values


def parse_where(command):
    """Проверяет корректность фильтрации таблицы"""
    parts = command.split("=")
    if len(parts) != 2:
        raise ValueError("Неверная команда")
    column_name = parts[0].strip()
    value = parts[1].strip()
    if value.startswith('"') and value.endswith('"'):
        parsed_value = value[1:-1]
    elif value.lower() == "true":
        parsed_value = True
    elif value.lower() == "false":
        parsed_value = False
    else:
        parsed_value = int(value)
    return {column_name: parsed_value}


def parse_select(command):
    """Проверяет корректность выборки таблицы"""
    parts = command.split("where", 1)
    command_parts = parts[0].split()
    if (len(command_parts) != 3 or command_parts[0] != "select"
            or command_parts[1] != "from"):
        raise ValueError("Неверная команда")
    table_name = command_parts[2]
    if len(parts) == 1:
        search_place = None
    else:
        search_place = parse_where(parts[1].strip())
    return table_name, search_place


def parse_delete(command):
    """Проверяет корректность удаления таблицы"""
    parts = command.split("where", 1)
    command_parts = parts[0].split()
    if (len(command_parts) != 3 or command_parts[0] != "delete"
            or command_parts[1] != "from"):
        raise ValueError("Неверная команда")
    if len(parts) != 2 or not parts[1].strip():
        raise ValueError("Неверная команда")
    table_name = command_parts[2]
    where_clause = parse_where(parts[1].strip())
    return table_name, where_clause


def parse_info(command):
    """Проверяет корректность вывода информации о таблице"""
    parts = command.split()
    if len(parts) != 2 or parts[0] != "info":
        raise ValueError("Неверная команда")
    return parts[1]


def parse_update(command):
    """Проверяет корректность обновления таблицы"""
    parts = command.split("where", 1)
    if len(parts) != 2:
        raise ValueError("Неверная команда")
    command_parts = parts[0].split("set", 1)
    if len(command_parts) != 2:
        raise ValueError("Неверная команда")
    main_parts = command_parts[0].split()
    if (len(main_parts) != 2 or main_parts[0] != "update"):
        raise ValueError("Неверная команда")
    table_name = main_parts[1]
    set_clause = parse_where(command_parts[1].strip())
    where_clause = parse_where(parts[1].strip())
    return table_name, set_clause, where_clause
