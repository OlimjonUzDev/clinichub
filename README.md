# ClinicHub — Backend

ClinicHub — klinikalarni boshqarish tizimining backend API'si. Django REST Framework asosida yozilgan, JWT autentifikatsiya, Stripe to'lovlari va Swagger hujjatlari bilan.

Frontend (admin panel, patient portal, doctor portal) alohida repoda joylashgan.

## Texnologiyalar

Python 3.12 · Django 6 · Django REST Framework · SimpleJWT · PostgreSQL · Stripe · drf-yasg (Swagger/ReDoc) · django-cors-headers · WhiteNoise · Docker

## Modullar (Django app'lar)

| App | Vazifasi |
|---|---|
| `users` | Registratsiya, login, rollar (admin / doctor / patient), JWT |
| `catalog` | Mutaxassisliklar, rank turlari va narxlari |
| `clinics` | Klinikalar va tibbiyot markazlari |
| `doctors` | Shifokorlar, ish jadvali, reytinglar |
| `patients` | Bemorlar |
| `appointments` | Uchrashuvlar (vaqt kesishuvi va ish jadvali tekshiruvi bilan) |
| `billing` | Invoyslar, shifokor to'lovlari |
| `payments` | To'lovlar, Stripe integratsiyasi va webhook |
| `prescriptions` | Retseptlar |
| `chat` | Bemor va shifokor o'rtasidagi chat |
| `notifications` | Bildirishnomalar, SMS (Infobip) |

## Talablar

- Python 3.12
- PostgreSQL (yoki Docker)

## O'rnatish va ishga tushirish

### Lokal

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env faylini yarating (pastdagi jadvalga qarang)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver      # http://127.0.0.1:8000
```

### Docker

```bash
docker compose up --build
```

`web` (port 8000) va `db` (PostgreSQL, port 5432) servislari ko'tariladi. `.env` fayli kerak. Birinchi ishga tushirishdan keyin migratsiyalarni qo'llang:

```bash
docker compose exec web python manage.py migrate
```

## Muhit o'zgaruvchilari (`.env`)

| O'zgaruvchi | Tavsif | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key (majburiy) | — |
| `DEBUG` | `True` bo'lsa debug rejimi va Swagger yoqiladi | `False` |
| `DJANGO_ALLOWED_HOSTS` | Vergul bilan ajratilgan hostlar | `localhost,127.0.0.1` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | PostgreSQL | `test_db`, `postgres`, `postgres` |
| `DB_HOST`, `DB_PORT` | PostgreSQL manzili | `localhost`, `5432` |
| `STRIPE_PUBLIC_KEY` | Stripe publishable key | — |
| `STRIPE_SECRET_KEY` | Stripe secret key | — |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook imzosi uchun secret | — |
| `CORS_ALLOWED_ORIGINS` | Qo'shimcha frontend originlari (vergul bilan) | — |
| `CSRF_TRUSTED_ORIGINS` | Ishonchli originlar (vergul bilan) | — |
| `SMS_OTP_ENABLED` | SMS OTP ni yoqish (`True`/`False`) | `False` |
| `INFOBIP_API_KEY`, `INFOBIP_BASE_URL` | Infobip SMS xizmati | — |

`localhost:5173`, `5174` va `5175` originlari CORS'da doim ruxsat etilgan (frontend ilovalarning dev portlari).

## API

Barcha endpoint'lar `/api/v1/` ostida:

| Prefiks | Modul |
|---|---|
| `/api/v1/` | `users` (registratsiya, login) |
| `/api/v1/auth/token/` | JWT: olish, `refresh/`, `verify/`, `logout/` (blacklist) |
| `/api/v1/catalog/`, `/clinics/`, `/doctors/`, `/patients/` | Ma'lumotnomalar |
| `/api/v1/appointments/` | Uchrashuvlar |
| `/api/v1/billing/`, `/payments/` | Invoys va to'lovlar |
| `/api/v1/prescriptions/` | Retseptlar |
| `/api/v1/chat/`, `/notifications/` | Chat va bildirishnomalar |

Autentifikatsiya: `Authorization: Bearer <access_token>`.

**Swagger hujjatlari** faqat `DEBUG=True` bo'lganda mavjud:
- Swagger UI — `http://127.0.0.1:8000/`
- ReDoc — `http://127.0.0.1:8000/redoc/`

Django admin — `/admin/`.

## Xavfsizlik

- Registratsiyada `role` mijozdan qabul qilinmaydi (default `patient`)
- Parol Django validatorlaridan o'tadi
- Throttling: anonim — 20/min, avtorizatsiyalangan — 60/min
- CORS faqat ruxsat etilgan originlar uchun
- `DEBUG=False` da HTTPS redirect va secure cookie'lar yoqiladi

## Testlar

```bash
python manage.py test
```

Testlar PostgreSQL ulanishini talab qiladi (`DB_*` o'zgaruvchilari). To'liq ishga tushirish taxminan 2 daqiqa oladi.

## CI

GitHub Actions (`.github/workflows/django-ci.yml`) `main` ga push va pull request'larda PostgreSQL 16 bilan `manage.py test` ni ishga tushiradi. Kerakli secret'lar: `SECRET_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `INFOBIP_API_KEY`.

## Litsenziya

[MIT](./LICENSE)
