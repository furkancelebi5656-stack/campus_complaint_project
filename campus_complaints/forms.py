from django import forms
from .models import Complaint, Assignment, ResolutionNote

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'title', 'description', 'priority']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['staff']

class StatusUpdateForm(forms.ModelForm):
    note = forms.CharField(widget=forms.Textarea, required=False, label='Çözüm Notu')
    class Meta:
        model = Complaint
        fields = ['status']
