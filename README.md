# MarketPulse

Перед запуском проекта убедитесь, что docker уже установлен на вашей машине🤝

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
    #     'HOST': 'postgres',
    #     'PORT': '5432',
    # }
}
```

Шаги по миграции:
1. Если остались прошлые файлы - удалить их, кроме `__init__.py`
2. Выполнить команду `python manage.py makemigrations`, можно добавить флаг `--settings=lyalya.settings_test` для тестовой БД
3. Выполнить команду `python manage.py migrate`, можно добавить флаг `--settings=lyalya.settings_test` для тестовой БД
4. Запустить тесты `python manage.py test core.tests.models`, можно добавить флаг `--settings=lyalya.settings_test` для тестовой БД, если все тесты пройдены успешно - миграция выполнена успешно

Локальный запуск frontend:
1. В директории frontend выполнить установку зависимостей `npm install`
2. Из директории frontend выполнить команду `"npm run dev`

Создание на сервере docker swarm manager (используется для бесшовного запуска):
1. Вызвать команду по первоначальному созданию swarm manager:
```
sudo docker swarm init
```
2. Преобразуем файл docker-compose для работы в docker swarm:
```
sudo docker stack deploy --compose-file docker-compose.yml myapp
```
`myapp` - это имя стека, по которому можно проводить запросы и манипуляции
3. Для просмотра запущенного сервиса можно воспользоваться следующим:
```
sudo docker service ls
```
4. Ручной перезапуск сервиса:
```
sudo docker service update --force name_service
```

Перезапуск docker swarm:
```
sudo docker swarm leave --force
sudo rm -rf /var/lib/docker/swarm/*
sudo docker swarm init
```