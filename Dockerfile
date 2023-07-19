FROM python:3.9

ENV DJANGO_ENV=production

ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y postgresql  \
    && apt-get install -y gettext  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8005

CMD python purchase/manage.py migrate && python purchase/manage.py compilemessages && python purchase/manage.py runserver $LISTEN_ADDR
