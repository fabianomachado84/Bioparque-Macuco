from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    role = models.CharField(max_length=100)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.role}"



# Instructor
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    class_obj = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE, related_name='instructors')

    def __str__(self):
        return f"{self.employee.user.first_name} em {self.class_obj}"

    # Basic Info
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True,help_text="Breve currículo do Instrutor")
    specialty = models.CharField(max_length=100, help_text="Ex: Matemática,Programação, Python, etc...")
    
    # Internal Control
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructors"
        ordering = ['name']

        def __str__(self)-> str:
            return f"{self.name} ({self.specialty})"
