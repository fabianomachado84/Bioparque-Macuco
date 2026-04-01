from enum import unique
from django.db import models
from django.db.models.base import class_prepared
from django.db.models.fields import return_None
from django.utils.text import capfirst

# Course / Curso
class Course(models.Model):
    STATUS_CHOICES = [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ]
            

    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_hours = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='active')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

# Class / Turma
class Class(models.Model):
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,related_name='classes')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField()


    def __str__(self):
        return f"{self.course.name} - {self.start_date}"

# Student / Aluno
class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    phone = models.CharField(max_length=255)
    emergency_contact = models.CharField(max_length=255)


    def __str__(self):
        return self.name 

# Enrollment / Inscrição
class Enrollment(models.Model):
    STATUS_CHOICES = [
            ('pending','Pending'),
            ('approved','Approved'),
            ('rejected','Rejected')
            ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='active')
    is_overbooked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'class_obj')

    def save(self, *args, **kwargs):
        if self.class_obj.enrollment_set.count() >= self.class_obj.capacity:
            self.is_overbooked = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.class_obj}"
