from django.contrib import admin
from .models import Teacher, Student, Course, Result


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'subject_speciality')
    search_fields = ('full_name', 'subject_speciality')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number')
    search_fields = ('full_name', 'roll_number')
    

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    search_fields = ('name', 'code')
    list_filter = ('teacher',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks_obtained')
    list_filter = ('course', 'student')
    search_fields = ('student__full_name', 'course__name')