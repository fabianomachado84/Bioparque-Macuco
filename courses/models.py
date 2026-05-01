from django.db import models

# Course #
class Course(models.Model):
    STATUS_CHOICES = [('active','Active'),('inactive','Inactive')]

    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_hours = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.name)

# Lesson
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='lessons')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField()
    instructor = models.ForeignKey('accounts.Instructor',on_delete=models.PROTECT,related_name='lessons')
    label = models.CharField(
        max_length=100, blank=True,
        help_text="Nome opcional da turma (ex: 'Turma escola Eusébio Farias'). Se vazio, usa numeração automática."
    )
    is_private = models.BooleanField(
        default=False,
        help_text="Turma fechada: não aparece na listagem pública e só admin pode inscrever alunos."
    )

    def __str__(self) -> str:
        suffix = self.label or str(self.start_date)
        return f"{self.course.name} - {suffix}"

