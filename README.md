# EduRelevance 🧠

**Ta'lim resurslarining dolzarbligini NLP yordamida avtomatik baholash tizimi**

---

## O'rnatish

### 1. Loyihani yuklab oling va papkani oching
```
cd edurelevance
```

### 2. Virtual environment yarating
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

### 4. .env faylini yarating
```bash
copy .env.example .env
```

**.env faylini oching va to'ldiring:**
```
SECRET_KEY=django-insecure-your-random-secret-key
DEBUG=True
DB_NAME=edurelevance
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 5. PostgreSQL bazasini yarating
```sql
CREATE DATABASE edurelevance;
```

### 6. Migratsiyalarni bajaring
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Superuser yarating (admin uchun)
```bash
python manage.py createsuperuser
```

### 8. Serverni ishga tushiring
```bash
python manage.py runserver
```

---

## Havolalar

| Sahifa | URL |
|--------|-----|
| Asosiy sayt | http://127.0.0.1:8000 |
| Admin panel | http://127.0.0.1:8000/admin |
| Kirish | http://127.0.0.1:8000/accounts/login |
| Ro'yxatdan o'tish | http://127.0.0.1:8000/accounts/register |

---

## OpenRouter API kaliti olish

1. https://openrouter.ai saytiga kiring
2. Ro'yxatdan o'ting (bepul)
3. API Keys bo'limidan yangi kalit yarating
4. Kalitni `.env` faylidagi `OPENROUTER_API_KEY` ga qo'ying

---

## Texnologiyalar

- **Backend**: Django 5.2 + DRF
- **Database**: PostgreSQL
- **AI/NLP**: OpenRouter (Llama 3.1 8B - bepul)
- **Admin**: Jazzmin (dark theme)
- **Frontend**: Django Templates (Cyber Dark dizayn)
- **PDF**: PyPDF2
- **URL scraping**: BeautifulSoup4
