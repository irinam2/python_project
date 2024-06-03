Смените настройки подключения к СУБД на свои в medical_app_django/settings.py в переменной DATABASES  
Откройте командную строку (cmd) или терминал в директории medical_app_django.   
Создайте виртуальное окружение (conda create --name conda_venv python=3.8).  
Активируйте виртуальное окружение (conda activate conda_venv).   
Установите необходимые библиотеки: pip install  -r requirements.txt   
Выполнить миграции:  
    python manage.py makemigrations services  
    python manage.py migrate services  
    python manage.py makemigrations services  
    python manage.py migrate services  
Запустите проект python manage.py runserver  