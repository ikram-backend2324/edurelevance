@echo off
echo ====================================
echo   EduRelevance - O'rnatish
echo ====================================

echo [1/4] Virtual environment yaratilmoqda...
python -m venv venv
call venv\Scripts\activate

echo [2/4] Kutubxonalar o'rnatilmoqda...
pip install -r requirements.txt

echo [3/4] .env fayl yaratilmoqda...
if not exist .env (
    copy .env.example .env
    echo .env fayl yaratildi. Iltimos .env faylini tahrirlang!
)

echo [4/4] Ma'lumotlar bazasi migratsiyalari...
python manage.py makemigrations
python manage.py migrate

echo.
echo ====================================
echo   Superuser yarating:
echo   python manage.py createsuperuser
echo.
echo   Serverni ishga tushiring:
echo   python manage.py runserver
echo ====================================
pause
