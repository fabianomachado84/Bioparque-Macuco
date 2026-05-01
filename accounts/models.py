from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    role = models.CharField(max_length=100)
    hire_date = models.DateField()

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Instructor
class Instructor(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    bio = models.TextField(blank=True,help_text="Breve currículo do Instrutor")
    specialty = models.CharField(max_length=100, help_text="Ex: Matemática,Programação, Python, etc...")

    class Meta:
        verbose_name = "Instrutor"
        verbose_name_plural = "Instrutores"
        ordering = ['employee__user__first_name']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} ({self.specialty})"

