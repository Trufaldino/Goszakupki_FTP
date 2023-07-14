# Goszakupki_FTP

1. Use scripts to create and update tables 
```bash
python3 ftp_sync.py
```

```bash
python3 import_purchase.py 
```

```bash
python3 import_required_files.py
```

```bash
python3 insert_into_django_tables.py
```

2. Create .env file and setup connection parameters
```bash
cp .env.template .env
nano .env
```

3. Run docker compose
```bash
docker compose up --build
```

4. Log in
```bash
http://localhost:8001/
```