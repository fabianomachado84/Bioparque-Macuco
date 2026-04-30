from rest_framework import serializers
from .models import Employee, Instructor

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'role', 'hire_date']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['id', 'employee', 'bio', 'specialty']