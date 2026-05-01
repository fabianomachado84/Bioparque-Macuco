from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):

    class Meta:
        verbose_name = "Funcionário"
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='employee_profile',
        verbose_name="Usuário",
    )
    role = models.CharField("Cargo", max_length=100)
    hire_date = models.DateField("Data de contratação")

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def display_name(self) -> str:
        """Full name when available, falls back to username."""
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return f"{self.display_name()} - {self.role}"

# Instructor
class Instructor(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        verbose_name="Funcionário",
    )

    bio = models.TextField(
        "Biografia",
        blank=True,
        help_text="Breve currículo do instrutor.",
    )
    specialty = models.CharField(
        "Especialidade",
        max_length=100,
        help_text="Ex: Biologia marinha, Trilhas, Educação ambiental, etc.",
    )

    class Meta:
        verbose_name = "Instrutor"
        verbose_name_plural = "Instrutores"
        ordering = ['employee__user__first_name']

    def __str__(self):
        return f"{self.employee.display_name()} ({self.specialty})"

