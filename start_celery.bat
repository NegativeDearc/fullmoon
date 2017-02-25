@echo off
set "d=%cd%"
call "%d%\venv\Scripts\activate.bat"
python -m celery -A app.tools.tasks.celery worker --loglevel=debug
pause