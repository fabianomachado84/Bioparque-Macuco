from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Enrollment, Payment, Student
from .serializers import (
    EnrollmentSerializer,
    PaymentSerializer,
    StudentSerializer
)

from .reports import (
    get_revenue_by_course_and_month,
    get_donations_by_type,
    get_students_age_groups
)


@api_view(['GET'])
@permission_classes([AllowAny])
def revenue_by_course_and_month(request):
    payments = get_revenue_by_course_and_month()
    return Response(payments)


@api_view(['GET'])
@permission_classes([AllowAny])
def donations_by_type(request):
    donations = get_donations_by_type()
    return Response(donations)


@api_view(['GET'])
@permission_classes([AllowAny])
def students_age_groups(request):
    age_groups = get_students_age_groups()
    return Response(age_groups)


def admin_reports(request):
    revenue = get_revenue_by_course_and_month()
    donations = get_donations_by_type()
    age_groups = get_students_age_groups()

    context = {
        'revenue': revenue,
        'donations': donations,
        'age_groups': age_groups,
    }

    return render(
        request,
        'admin/reports.html',
        context
    )


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer