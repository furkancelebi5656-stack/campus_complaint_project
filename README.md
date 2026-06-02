# Kampüs Şikayet ve Talep Yönetim Sistemi

Bu klasör Django tabanlı proje iskeletidir. Raporla uyumlu olarak öğrenci, personel ve yönetici rollerini; şikayet oluşturma, atama, durum güncelleme ve raporlama mantığını içerir.

## Kurulum
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
django-admin startproject config .
python manage.py startapp campus_complaints
# Bu klasördeki dosyaları oluşturulan app içine kopyalayın.
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Roller
- STUDENT: Şikayet oluşturur ve kendi şikayetlerini takip eder.
- STAFF: Kendisine atanan şikayetleri görüntüler ve durum günceller.
- ADMIN: Tüm kayıtları yönetir, personele atama yapar ve raporları görür.
