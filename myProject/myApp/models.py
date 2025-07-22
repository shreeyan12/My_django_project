from django.db import models
from django.contrib.auth.models import User

# 1. Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    

    def __str__(self):
         return f"{self.full_name} ({self.roll_number})"

# 2. Teacher Model    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    subject_speciality = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

# 3. Course Model
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    students = models.ManyToManyField(Student, related_name='courses')  # many-to-many with students

    def __str__(self):
        return f"{self.name} ({self.code})"

# 4. Result Model
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.FloatField()

    class Meta:
        unique_together = ('student', 'course')  # Prevent duplicate result entry

    def __str__(self):
        return f"{self.student.full_name} - {self.course.name}: {self.marks_obtained}"