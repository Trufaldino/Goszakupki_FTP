import sqlite3
import zipfile
import xml.etree.ElementTree as ET

conn = sqlite3.connect('ftp_purchase/database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM purchase_files WHERE status = 'new'")
files = cursor.fetchall()

for file in files:
    file_id, filename, file_date, import_date, record_count, status = file

    # Обработка .zip архива
    try:
        with zipfile.ZipFile(f'./downloads/{filename}') as zip_file:
            if not zip_file.namelist():
                cursor.execute("UPDATE purchase_files SET status = 'empty_file' WHERE id = ?", (file_id,))
                conn.commit()
                continue

            # Поиск .xml файлов внутри архива
            xml_files = [f for f in zip_file.namelist() if f.endswith('.xml')]

            if not xml_files:
                cursor.execute("UPDATE purchase_files SET status = 'error' WHERE id = ?", (file_id,))
                conn.commit()
                continue

            cursor.execute("CREATE TABLE IF NOT EXISTS purchase_plan (id INTEGER PRIMARY KEY, externalId TEXT, planNumber TEXT, versionNumber TEXT, filename TEXT, archive_name TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS purchase (id INTEGER PRIMARY KEY, externalId TEXT, total_price REAL, purchase_object_info TEXT, publish_year INTEGER, purchase_files INTEGER, FOREIGN KEY (purchase_files) REFERENCES purchase_files(id), FOREIGN KEY (externalId) REFERENCES purchase_plan(externalId))")
            
            for xml_file in xml_files:
                xml_data = zip_file.read(xml_file)
                xml_root = ET.fromstring(xml_data)

                namespace = {'ns1': 'http://zakupki.gov.ru/oos/types/1'}
                external_id = xml_root.find('.//ns1:id', namespace).text.strip() if xml_root.find('.//ns1:id', namespace) is not None else ''
                plan_number = xml_root.find('.//ns1:planNumber', namespace).text.strip() if xml_root.find('.//ns1:planNumber', namespace) is not None else ''
                version_number = xml_root.find('.//ns1:versionNumber', namespace).text.strip() if xml_root.find('.//ns1:versionNumber', namespace) is not None else ''

                cursor.execute("INSERT INTO purchase_plan (externalId, planNumber, versionNumber, filename, archive_name) VALUES (?, ?, ?, ?, ?)",
                            (external_id, plan_number, version_number, xml_file, filename))

                publish_year = xml_root.find('.//ns1:publishYear', namespace).text.strip() if xml_root.find('.//ns1:publishYear', namespace) is not None else ''
                total_price = xml_root.find('.//ns1:totalPurchaseFinances/ns1:total', namespace).text.strip() if xml_root.find('.//ns1:totalPurchaseFinances/ns1:total', namespace) is not None else ''
                purchase_object_info = xml_root.find('.//ns1:purchaseObjectInfo', namespace).text.strip() if xml_root.find('.//ns1:purchaseObjectInfo', namespace) is not None else ''

                cursor.execute("INSERT INTO purchase (externalId, total_price, purchase_object_info, publish_year, purchase_files) VALUES (?, ?, ?, ?, ?)",
                            (external_id, total_price, purchase_object_info, publish_year, file_id))

                conn.commit()

            cursor.execute("UPDATE purchase_files SET status = 'done' WHERE id = ?", (file_id,))
            conn.commit()

    except zipfile.BadZipFile:
        cursor.execute("UPDATE purchase_files SET status = 'error' WHERE id = ?", (file_id,))
        conn.commit()

conn.close()

print("Таблицы purchase_plan и purchase созданы")
