import os
import re
from datetime import datetime
import psycopg2
from dotenv import load_dotenv


load_dotenv()


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
    conn = psycopg2.connect(
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host="localhost",
        port=os.environ.get("DB_PORT")
    )
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS purchase_files (id SERIAL PRIMARY KEY, filename TEXT, file_date DATE, import_date TIMESTAMP, record_count INTEGER, status TEXT)")

    conn.commit()
    conn.close()


def check_and_insert_file(filename):
    conn = psycopg2.connect(
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host="localhost",
        port=os.environ.get("DB_PORT")
    )
    c = conn.cursor()

    relative_path = os.path.relpath(filename, directory)
    c.execute("SELECT filename FROM purchase_files WHERE filename = %s", (relative_path,))
    result = c.fetchone()

    if not result:
        file_date = re.search(r"_(\d{10})_", filename).group(1)
        file_date = datetime.strptime(file_date, "%Y%m%d%H").date()
        import_date = datetime.now()

        c.execute("SELECT COUNT(*) FROM purchase_files")
        count_result = c.fetchone()
        record_count = count_result[0] + 1 if count_result else 1
        
        status = "new"

        c.execute("INSERT INTO purchase_files (filename, file_date, import_date, record_count, status) VALUES (%s, %s, %s, %s, %s)",
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
