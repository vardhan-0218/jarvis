@echo off
echo Jarvis AI Assistant Setup
echo ========================

echo Installing required packages...
pip install -r requirements.txt

echo.
echo Initializing database...
python -c "from Backend.db import initialize_database; initialize_database()"

echo.
echo Setup completed!
echo.
echo To start Jarvis:
echo 1. Run: python main.py (for single process)
echo 2. Run: python run.py (for multi-process with hotword)
echo.
pause
