from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Öğrenci'),
        ('STAFF', 'Personel'),
        ('ADMIN', 'Yönetici'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Açık'),
        ('IN_PROGRESS', 'İşlemde'),
        ('RESOLVED', 'Çözüldü'),
        ('REJECTED', 'Reddedildi'),
    ]
    PRIORITY_CHOICES = [('LOW','Düşük'),('MEDIUM','Orta'),('HIGH','Yüksek')]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    complaint = models.OneToOneField(Complaint, on_delete=models.CASCADE, related_name='assignment')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_complaints')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assignments_made')
    assigned_at = models.DateTimeField(auto_now_add=True)

class ResolutionNote(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='notes')
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
