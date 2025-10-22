@echo off
echo Starting WorkMate Backend Server...
cd Backend
call venv\Scripts\activate
python app.py
pause
