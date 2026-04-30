from rest_framework import serializers
from .models import Enrollment, Payment, Student

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'lesson', 'enrollment_date', 'status', 'is_overbooked']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'enrollment', 'payment_date', 'payment_method', 'payment_origin', 'status', 'money_amount', 'item_quantity_kg', 'approved_by']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'cpf', 'phone', 'emergency_contact']