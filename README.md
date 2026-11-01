# املاک — فاز اول

محتوای این پوشه فقط موارد فاز اول است:

1. **تعریف وب اپلیکیشن‌ها**: `accounts`, `properties`, `inquiries`, `core` و تنظیمات در `config/settings.py`
2. **طراحی فرایندها**: ۵ نمودار مستقل در `docs/process-diagrams/` (هر کدام با نقش‌ها، تصمیم‌ها و مسیرهای خطا) و توضیح هر فرایند (هدف، نقش‌ها، مراحل) در `docs/phase1-report.md`
3. **طراحی و تعریف مدل‌ها**: فایل `models.py` هر اپ + migrationها + نمودار `docs/er-diagram.png`

(view، url، template، form و داده‌ی تستی مربوط به فازهای بعدی است و در این پوشه نیست.)

گزارش کامل: [docs/phase1-report.md](docs/phase1-report.md)

## اجرا (اختیاری)

```sh
docker compose up --build
```

سپس ساخت کاربر ادمین و مشاهده‌ی مدل‌ها در <http://localhost:8000/admin/>:

```sh
docker compose exec web python manage.py createsuperuser
```
