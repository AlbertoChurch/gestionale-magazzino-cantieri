@echo off
cd /d "%~dp0.."
if not exist logs mkdir logs
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 >> logs\server.log 2>&1
