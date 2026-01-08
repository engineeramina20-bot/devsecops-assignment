# [span_10](start_span)استخدام صورة خفيفة وآمنة[span_10](end_span)
FROM python:3.9-slim-buster

# إنشاء مستخدم غير root للأمان
RUN useradd -m devsecops

WORKDIR /app

# نسخ الملفات وتغيير الملكية
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .
RUN mkdir uploads && chown -R devsecops:devsecops /app

# التبديل للمستخدم غير الصلاحيات المطلقة
USER devsecops

EXPOSE 5000

# تشغيل التطبيق
CMD ["python", "app.py"]