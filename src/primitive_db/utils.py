import json
import os

from .constants import DATA_DIR

def load_metadata(filepath):
    """Загружает метаданные из файла"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {}
    return data


def load_table_data(table_name):
    """Загружает метаданные таблиц изфайла"""
    try:
        with open(f"{DATA_DIR}/{table_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    return data


def save_metadata(filepath, data):
    """Сохраняет метаданные в файл"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_table_data(table_name, data):
    """Сохраняет метаданные таблицы в файл"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(f"{DATA_DIR}/{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
