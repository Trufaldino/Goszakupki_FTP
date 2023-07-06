# Goszakupki_FTP

1. Install django
```
pip install django
```

2. Make migrations
```
python3 ftp_purchase/manage.py migrate
```

3. Use scripts to create and update tables 
```
python3 ftp_sync.py
```

```
python3 import_purchase.py 
```

```
python3 script.py 
```

```
python3 insert.py 
```

4. Run server
```
python3  ftp_purchase/manage.py runserver
```