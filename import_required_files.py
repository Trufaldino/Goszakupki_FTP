import os
import zipfile
import xml.etree.ElementTree as ET
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def process_zip_file(file_id, filename):
    try:
        with zipfile.ZipFile(f'./downloads/{filename}') as zip_file:
            if not zip_file.namelist():
                cursor.execute("UPDATE purchase_files SET status = 'empty_file' WHERE id = %s", (file_id,))
                conn.commit()
                return

            xml_files = [f for f in zip_file.namelist() if f.endswith('.xml')]

            if not xml_files:
                cursor.execute("UPDATE purchase_files SET status = 'error' WHERE id = %s", (file_id,))
                conn.commit()
                return

            for xml_file in xml_files:
                xml_data = zip_file.read(xml_file)
                xml_root = ET.fromstring(xml_data)

                namespace = {'ns1': 'http://zakupki.gov.ru/oos/types/1'}
                external_id = xml_root.find('.//ns1:id', namespace).text.strip() if xml_root.find('.//ns1:id', namespace) is not None else ''
                plan_number = xml_root.find('.//ns1:planNumber', namespace).text.strip() if xml_root.find('.//ns1:planNumber', namespace) is not None else ''
                version_number = xml_root.find('.//ns1:versionNumber', namespace).text.strip() if xml_root.find('.//ns1:versionNumber', namespace) is not None else ''

                cursor.execute("INSERT INTO purchase_plan (externalId, planNumber, versionNumber, filename, archive_name) VALUES (%s, %s, %s, %s, %s)",
                            (external_id, plan_number, version_number, xml_file, filename))

                publish_year = xml_root.find('.//ns1:publishYear', namespace).text.strip() if xml_root.find('.//ns1:publishYear', namespace) is not None else ''
                total_price = xml_root.find('.//ns1:totalPurchaseFinances/ns1:total', namespace).text.strip() if xml_root.find('.//ns1:totalPurchaseFinances/ns1:total', namespace) is not None else None
                purchase_object_info = xml_root.find('.//ns1:purchaseObjectInfo', namespace).text.strip() if xml_root.find('.//ns1:purchaseObjectInfo', namespace) is not None else ''

                cursor.execute("INSERT INTO purchase (externalId, total_price, purchase_object_info, publish_year, purchase_files) VALUES (%s, %s, %s, %s, %s)",
                            (external_id, total_price, purchase_object_info, publish_year, file_id))

            cursor.execute("UPDATE purchase_files SET status = 'done' WHERE id = %s", (file_id,))
            conn.commit()

    except zipfile.BadZipFile:
        cursor.execute("UPDATE purchase_files SET status = 'error' WHERE id = %s", (file_id,))
        conn.commit()


conn = psycopg2.connect(
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host="localhost",
    port=os.environ.get("DB_PORT")
    )
cursor = conn.cursor()
cursor = conn.cursor()

cursor.execute("SELECT * FROM purchase_files WHERE status = 'new'")
files = cursor.fetchall()

cursor.execute("CREATE TABLE IF NOT EXISTS purchase_plan (id SERIAL PRIMARY KEY, externalId TEXT UNIQUE, planNumber TEXT, versionNumber TEXT, filename TEXT, archive_name TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS purchase (id SERIAL PRIMARY KEY, externalId TEXT, total_price REAL, purchase_object_info TEXT, publish_year INTEGER, purchase_files INTEGER, FOREIGN KEY (purchase_files) REFERENCES purchase_files(id), FOREIGN KEY (externalId) REFERENCES purchase_plan(externalId))")
conn.commit()

for file in files:
    file_id, filename, file_date, import_date, record_count, status = file
    process_zip_file(file_id, filename)

conn.close()

print("Таблицы purchase_plan и purchase созданы")
