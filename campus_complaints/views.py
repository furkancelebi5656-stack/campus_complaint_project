from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, Assignment, Profile, ResolutionNote
from .forms import ComplaintForm, AssignmentForm, StatusUpdateForm

def role_required(*roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if not request.user.is_authenticated or not profile or profile.role not in roles:
                messages.error(request, 'Bu işlem için yetkiniz yok.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@login_required
def dashboard(request):
    role = request.user.profile.role
    if role == 'STUDENT':
        complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')
    elif role == 'STAFF':
        complaints = Complaint.objects.filter(assignment__staff=request.user).order_by('-created_at')
    else:
        complaints = Complaint.objects.all().order_by('-created_at')
    return render(request, 'campus_complaints/dashboard.html', {'complaints': complaints})

@login_required
@role_required('STUDENT')
def create_complaint(request):
    form = ComplaintForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        complaint = form.save(commit=False)
        complaint.student = request.user
        complaint.save()
        messages.success(request, 'Şikayet başarıyla oluşturuldu.')
        return redirect('dashboard')
    return render(request, 'campus_complaints/form.html', {'form': form, 'title': 'Yeni Şikayet'})

@login_required
@role_required('ADMIN')
def assign_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    form = AssignmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Assignment.objects.update_or_create(
            complaint=complaint,
            defaults={'staff': form.cleaned_data['staff'], 'assigned_by': request.user}
        )
        messages.success(request, 'Şikayet personele atandı.')
        return redirect('dashboard')
    return render(request, 'campus_complaints/form.html', {'form': form, 'title': 'Personel Ata'})

@login_required
@role_required('STAFF')
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk, assignment__staff=request.user)
    form = StatusUpdateForm(request.POST or None, instance=complaint)
    if request.method == 'POST' and form.is_valid():
        form.save()
        note = form.cleaned_data.get('note')
        if note:
            ResolutionNote.objects.create(complaint=complaint, staff=request.user, note=note)
        messages.success(request, 'Durum güncellendi.')
        return redirect('dashboard')
    return render(request, 'campus_complaints/form.html', {'form': form, 'title': 'Durum Güncelle'})

@login_required
@role_required('ADMIN')
def reports(request):
    total = Complaint.objects.count()
    open_count = Complaint.objects.filter(status='OPEN').count()
    resolved = Complaint.objects.filter(status='RESOLVED').count()
    return render(request, 'campus_complaints/reports.html', {'total': total, 'open_count': open_count, 'resolved': resolved})
