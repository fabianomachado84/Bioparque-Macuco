from django.db import models
from django.db.models import UniqueConstraint, Q
from django.core.exceptions import ValidationError

import courses
from courses.models import Lesson



# Student
class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)


    def __str__(self) -> str:
        return str(self.name) 


# Enrollment 
class Enrollment(models.Model):
    STATUS_CHOICES = [('pending','Pending'), ('approved','Approved'), ('rejected','Rejected')]

    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='enrolments')
    class_obj = models.ForeignKey('courses.Lesson', on_delete=models.PROTECT, related_name='enrolments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_overbooked = models.BooleanField(default=False)

    class Meta:
        constraints = [UniqueConstraint( fields=['student', 'class_obj'], condition=~Q(status='rejected'), name='unique_active_enrolment' )]

    def clean(self):
        if not self.pk:
            count_atual = self.class_obj.enrolments.count()
            if count_atual >= self.class_obj.capacity:
                if not self.is_overbooked:
                    raise ValidationError("Turma lotada. Inscrição online não permitida.")

    def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.student} - {self.class_obj}"

# Payment
class Payment(models.Model):
    METHOD_CHOICES = [
        ('credit_card', 'Credit Card'), ('pix', 'Pix'), ('cash', 'Cash'),
        ('donation_item', 'Donation Item'), ('hybrid', 'Hybrid'), ('scholarship', 'Scholarship')
    ]
    STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed')]
    ORIGIN_CHOICES = [('online', 'Online'), ('in_person', 'In Person')]

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    payment_origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES, default='online')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Payment Methods ( Money or Donation Item )
    money_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_quantity_kg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Approved by  (Optional for online, mandatory for in-person)
    approved_by = models.ForeignKey('accounts.Employee', on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.payment_method == 'donation_item' and not self.item_quantity_kg:
            raise ValidationError("Para doações, informe a quantidade em kg.")
        
        if self.payment_origin == 'in_person' and not self.approved_by:
            raise ValidationError("Pagamentos presenciais precisam ser aprovados por um funcionário.")

    def __str__(self):
        return f"Pagamento {self.id} ({self.payment_method})"
