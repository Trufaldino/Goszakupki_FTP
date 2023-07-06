import os
import sqlite3
import re
from datetime import datetime


def get_latest_file(directory):
    latest_file = None
    latest_date = datetime.min

    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".xml.zip"):
                continue

            match = re.search(r"_(\d{10})_", file)
            if match:
                file_date = datetime.strptime(match.group(1), "%Y%m%d%H")
                if file_date > latest_date:
                    latest_date = file_date
                    latest_file = os.path.join(root, file)

    return latest_file


def create_database():
    conn = sqlite3.connect("ftp_purchase/database.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS purchase_files (id INTEGER PRIMARY KEY, filename TEXT, file_date TEXT, import_date TEXT, record_count INTEGER, status TEXT)")

    conn.commit()
    conn.close()

def check_and_insert_file(filename):
    conn = sqlite3.connect("ftp_purchase/database.db")
    c = conn.cursor()

    relative_path = os.path.relpath(filename, directory)
    c.execute("SELECT filename FROM purchase_files WHERE filename = ?", (relative_path,))
    result = c.fetchone()

    if not result:
        file_date = re.search(r"_(\d{10})_", filename).group(1)
        file_date = datetime.strptime(file_date, "%Y%m%d%H").strftime("%Y-%m-%d")
        import_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record_count = c.execute("SELECT COUNT(*) FROM purchase_files").fetchone()[0] + 1
        status = "new"

        c.execute("INSERT INTO purchase_files (filename, file_date, import_date, record_count, status) VALUES (?, ?, ?, ?, ?)",
                  (relative_path, file_date, import_date, record_count, status))

        print("Файл успешно добавлен в базу данных.")

    conn.commit()
    conn.close()


directory = "./downloads"  # Укажите путь к папке, в которой нужно искать файлы

for root, _, _ in os.walk(directory):
    latest_file = get_latest_file(root)

    if latest_file:
        create_database()
        check_and_insert_file(latest_file)
    else:
        print(f"В папке {root} не найдено файлов с расширением .xml.zip.")
