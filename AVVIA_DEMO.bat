@echo off
rem Avvia il gestionale con i dati di esempio: doppio clic e basta.
rem La prima volta prepara tutto da solo (qualche minuto), le volte dopo parte subito.
rem PORTA e SENZA_BROWSER si possono impostare prima di lanciarlo (servono per le prove).
cd /d "%~dp0"
if not defined PORTA set PORTA=8000

python --version >nul 2>&1
if errorlevel 1 (echo Python non e' installato, oppure non e' nel PATH. & echo Scaricalo da https://www.python.org/downloads/ e nella prima schermata dell'installazione spunta "Add python.exe to PATH". & echo Poi rilancia questo file. & pause & exit /b 1)

if not exist ".venv\Scripts\python.exe" (echo Preparo l'ambiente Python, solo la prima volta... & python -m venv .venv)
if errorlevel 1 (echo Non sono riuscito a creare l'ambiente Python. & pause & exit /b 1)

rem Se i componenti ci sono gia' non scarica nulla (e non serve internet).
".venv\Scripts\python.exe" -m pip install -q --disable-pip-version-check -r requirements.txt
if errorlevel 1 (echo Installazione dei componenti non riuscita: serve internet, e Python 3.14. & pause & exit /b 1)

rem Dati di esempio solo se il database non esiste o e' vuoto: non tocca mai dati gia' presenti.
set SEME=1
if exist gestionale.db for %%F in (gestionale.db) do if %%~zF GTR 0 set SEME=0
if "%SEME%"=="1" (".venv\Scripts\python.exe" deploy\dati_demo.py)
if errorlevel 1 (echo Non sono riuscito a creare i dati di esempio. & pause & exit /b 1)

echo.
echo Il gestionale parte su http://127.0.0.1:%PORTA%
echo Accedi con  admin@example.com  e password  demo1234
echo Per fermarlo chiudi questa finestra.
echo.
if not defined SENZA_BROWSER start "" /min cmd /c "timeout /t 4 /nobreak >nul & start http://127.0.0.1:%PORTA%"
".venv\Scripts\python.exe" -m uvicorn app.main:app --port %PORTA%
echo.
echo Il gestionale si e' fermato. Se vedi un errore di porta occupata, chiudi le altre finestre del gestionale e riprova.
pause
