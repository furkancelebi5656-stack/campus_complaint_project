from django.contrib import admin
from .models import Profile, Category, Complaint, Assignment, ResolutionNote

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Complaint)
admin.site.register(Assignment)
admin.site.register(ResolutionNote)
