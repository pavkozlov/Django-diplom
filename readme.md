## Документация по проекту

Для запуска проекта необходимо:

Установить зависимости:
```bash
pip install -r requirements.txt
```

Выполнить следующие команды:

* Команда для создания миграций приложения для базы данных
```bash
python manage.py migrate
```

* Команда для запуска приложения
```bash
python manage.py runserver
```

* При создании моделей или их изменении необходимо выполнить следующие команды:
```bash
python manage.py makemigrations
python manage.py migrate
```