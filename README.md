# MarketPulse

Чтобы запустить проект в docker:

1. Скачать проект.
2. В директории с docker-compose.yml запустить команды:

Если требуется остановить предыдущую версию проекта и удалить собранные образы (данные в volumes сохраняются):
```
sudo docker compose down
```

Если требуется остановить предыдущую версию проекта и удалить все сохраняемые данные:
```
sudo docker compose down -v
```

Для сборки проекта:
```
sudo docker compose up --build
```

Для сборки проекта в фоновом режиме:
```
sudo docker compose up --build -d
```

Для локального тестирования без `postgreSQL` необходимо изменить `settings.py`
Который расположен по пути `./backend/lyalya/lyalya/settings.py`
Код для замены:
```
DATABASES = {
    # # Для тестов и локального запуска 
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': { 
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'data_base_market_pulse',
    #     'USER': 'postgres',
    #     'PASSWORD': 'qwer4617',
    #     'HOST': 'my-postgres-2025',
    #     'PORT': '5432',
    # }
}
```