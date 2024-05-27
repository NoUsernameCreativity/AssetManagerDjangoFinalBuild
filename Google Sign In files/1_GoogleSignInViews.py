from django.shortcuts import render, redirect
from auth_app.models import teacher, student

# Create your views here.

def index(request):
    return render(
        request,
        'auth_app/index.html',
        {'content': 'hello'}
        )

def inputTeacherOrStudent(request):
    # check if user is already in database, in which case no action is required
    if teacher.objects.filter(user=request.user).exists():
        return redirect('/')
    if student.objects.filter(user=request.user).exists():
        return redirect('/')
    # post for teacher/student choice
    if request.method == "POST":
        if request.POST.get('teacherButton', None):
            teacher.objects.create(user=request.user, Area=request.POST.get('Area', None))
        else:
            student.objects.create(user=request.user)
        return redirect('/')
    return render(
        request,
        'auth_app/TeacherOrStudent.html',)
