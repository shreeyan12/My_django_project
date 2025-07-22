from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, StudentForm, TeacherForm,ResultForm,ResultSearchForm
from .models import Student, Teacher,Course,Result
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, 'myApp/home.html')


def register_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "Student registered successfully!")
            return redirect('login')
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'register_student.html', {
        'user_form': user_form,
        'student_form': student_form
    })

def register_teacher(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, "Teacher registered successfully!")
            return redirect('login')
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()
    return render(request, 'register_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'student'):
                return redirect('student_dashboard')
            elif hasattr(user, 'teacher'):
                return redirect('teacher_dashboard')
            else:
                return redirect('/')  
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('home')


# Teacher Dashboard: Add result
@login_required
def teacher_dashboard(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Access denied. Not a teacher.")
        return redirect('login')

    return render(request, 'teacher_dashboard.html')


 # Teacher adds marks
@login_required
def add_result(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Access denied.")
        return redirect('login')

    teacher = request.user.teacher

    if request.method == 'POST':
        form = ResultForm(teacher=teacher, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('view_results')
    else:
        form = ResultForm(teacher=teacher)

    return render(request, 'add_result.html', {'form': form})



@login_required
def view_results(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Access denied.")
        return redirect('login')

    teacher = request.user.teacher
    results = Result.objects.filter(course__teacher=teacher)

    return render(request, 'view_result.html', {'results': results})


@login_required
def edit_result(request, result_id):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Access denied.")
        return redirect('login')

    teacher = request.user.teacher
    result = Result.objects.get(id=result_id)


    if result.course.teacher != teacher:
        messages.error(request, "You can only edit your own course results.")
        return redirect('view_results')

    if request.method == 'POST':
        form = ResultForm(teacher=teacher, data=request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, "Result updated successfully.")
            return redirect('view_results')
    else:
        form = ResultForm(teacher=teacher, instance=result)

    return render(request, 'edit_result.html', {'form': form, 'result': result})



@login_required
def delete_result(request, result_id):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "Access denied.")
        return redirect('login')

    teacher = request.user.teacher
    result = Result.objects.get(id=result_id)

    if result.course.teacher != teacher:
        messages.error(request, "You can only delete your own course results.")
        return redirect('view_results')

    result.delete()
    messages.success(request, "Result deleted successfully.")
    return redirect('view_results')



@login_required
def student_dashboard(request):
    student = request.user.student
    result_data = None

    if request.method == 'POST':
        form = ResultSearchForm(student, request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            result_data = Result.objects.filter(student=student, course=course).first()
    else:
        form = ResultSearchForm(student)

    return render(request, 'student_dashboard.html', {
        'student': student,
        'form': form,
        'result_data': result_data
    })