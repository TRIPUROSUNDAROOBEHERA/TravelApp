@echo off

cd /d "%~dp0"

call venv\Scripts\activate

python -m pip install django

python manage.py runserver 127.0.0.1:8001

pause