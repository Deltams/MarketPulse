FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /backend

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py makemigrations --waitpg=1 && python manage.py migrate auth --waitpg=1 && python manage.py migrate core --waitpg=1 && python manage.py migrate --waitpg=1 &&  python manage.py runserver 0.0.0.0:8000"]