from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complaints/new/', views.create_complaint, name='create_complaint'),
    path('complaints/<int:pk>/assign/', views.assign_complaint, name='assign_complaint'),
    path('complaints/<int:pk>/status/', views.update_status, name='update_status'),
    path('reports/', views.reports, name='reports'),
]
