from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Result,Course


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'roll_number']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'subject_speciality']


class ResultForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none())
    student = forms.ModelChoiceField(queryset=Student.objects.none())

    class Meta:
        model = Result
        fields = ['student', 'course', 'marks_obtained']

    def __init__(self, teacher=None, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        if teacher:
            if isinstance(self.fields['course'], forms.ModelChoiceField):
                self.fields['course'].queryset = Course.objects.filter(teacher=teacher)
            if isinstance(self.fields['student'], forms.ModelChoiceField):
                self.fields['student'].queryset = Student.objects.filter(courses__teacher=teacher).distinct()




class ResultSearchForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.none(), label="Select Course")

    def __init__(self, student, *args, **kwargs):
        super(ResultSearchForm, self).__init__(*args, **kwargs)
        if isinstance(self.fields['course'], forms.ModelChoiceField):
            self.fields['course'].queryset = student.courses.all()
