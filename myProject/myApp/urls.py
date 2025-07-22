from django.urls import path
from myApp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-student/', views.register_student, name='register_student'),
    path('register-teacher/', views.register_teacher, name='register_teacher'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add_result/', views.add_result, name='add_result'),
    path('view_results/', views.view_results, name='view_results'),
    path('edit_result/<int:result_id>/', views.edit_result, name='edit_result'),
    path('delete_result/<int:result_id>/', views.delete_result, name='delete_result'),
     
]