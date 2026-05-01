from datetime import date, timedelta

from django.db import models
from django.db.models import UniqueConstraint, Q
from django.core.exceptions import ValidationError
from django.utils import timezone


# Default deadline for pending enrollments to be paid before they expire.
ENROLLMENT_EXPIRATION_HOURS = 24


def default_enrollment_expiration():
    """Default expiration timestamp for new pending enrollments."""
    return timezone.now() + timedelta(hours=ENROLLMENT_EXPIRATION_HOURS)



# Student
class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)
    birth_date = models.DateField(
        help_text="Data de nascimento. Usada para verificar restrições de idade em cursos e identificar menores que precisem de autorização."
    )

    class Meta:
        verbose_name = "Aluno"
        verbose_name_plural = "Alunos"

    @property
    def age(self) -> int:
        """Idade atual calculada a partir de birth_date."""
        today = date.today()
        years = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    @property
    def is_minor(self) -> bool:
        """Indica se o aluno é menor de idade (precisa de autorização do responsável)."""
        return self.age < 18

    def __str__(self) -> str:
        return str(self.name) 

# Enrollment 
class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='enrollments')
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.PROTECT, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_overbooked = models.BooleanField(default=False)
    expires_at = models.DateTimeField(
        null=True, blank=True,
        default=default_enrollment_expiration,
        help_text="Prazo para o pagamento ser confirmado. Se status ainda for 'pending' após este horário, vira 'expired' e a vaga é liberada."
    )

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        constraints = [UniqueConstraint(
            fields=['student', 'lesson'],
            condition=~Q(status__in=['rejected', 'expired']),
            name='unique_active_enrolment',
        )]

    def clean(self):
        if not self.pk:
            count_atual = self.lesson.enrollments.count()
            if count_atual >= self.lesson.capacity:
                if not self.is_overbooked:
                    raise ValidationError("Turma lotada. Inscrição online não permitida.")

    def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.student} - {self.lesson}"

# Payment
class Payment(models.Model):
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'), ('pix', 'Pix'), ('cash', 'Cash'),
        ('donation_item', 'Donation Item'), ('hybrid', 'Hybrid'), ('scholarship', 'Scholarship')
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed')]
    ORIGIN_CHOICES = [('online', 'Online'), ('in_person', 'In Person')]
    DONATION_TYPE_CHOICES = [
        ('dog_food', 'Ração de Cachorro'),
        ('cat_food', 'Ração de Gato'),
        ('bird_food', 'Ração de Pássaro'),
    ]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.PROTECT, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payment_origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES, default='online')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Payment Methods ( Money or Donation Item )
    money_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    donation_type = models.CharField(
        max_length=20, choices=DONATION_TYPE_CHOICES, blank=True,
        help_text="Tipo de ração doada. Obrigatório quando payment_method é 'donation_item' ou 'hybrid'."
    )
    
    # Approved by  (Optional for online, mandatory for in-person)
    approved_by = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def clean(self):
        if self.payment_method == 'donation_item' and not self.item_quantity_kg:
            raise ValidationError("Para doações, informe a quantidade em kg.")

        if self.payment_method in ('donation_item', 'hybrid') and not self.donation_type:
            raise ValidationError("Para pagamentos com ração, informe o tipo (cachorro, gato ou pássaro).")

        if self.payment_origin == 'in_person' and not self.approved_by:
            raise ValidationError("Pagamentos presenciais precisam ser aprovados por um funcionário.")

    def __str__(self):
        return f"Pagamento {self.id} ({self.payment_method})"
