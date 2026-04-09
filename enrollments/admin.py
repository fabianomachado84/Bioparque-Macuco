from django.contrib import admin
from .models import Student, Enrollment,Payment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'status', 'is_overbooked')
    list_filter = ('status', 'is_overbooked')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'enrollment', 'payment_method', 'money_amount', 'item_quantity_kg', 'status')
    list_filter = ('payment_method', 'status', 'payment_origin')
    search_fields = ('enrollment__student__name',)
