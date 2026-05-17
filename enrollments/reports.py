from django.db.models import Sum
from django.db.models.functions import TruncMonth

from .models import Payment, Student


def get_revenue_by_course_and_month():
    payments = (
        Payment.objects
        .filter(status='confirmed')
        .annotate(
            month=TruncMonth('payment_date')
        )
        .values(
            'month',
            'enrollment__lesson__course__name'
        )
        .annotate(
            total_revenue=Sum('money_amount')
        )
        .order_by('month')
    )

    return payments

def get_donations_by_type():
    donations = (
        Payment.objects
        .filter(
            status='confirmed',
            donation_type__isnull=False
        )
        .values('donation_type')
        .annotate(
            total_kg=Sum('item_quantity_kg')
        )
        .order_by('donation_type')
    )

    return donations

def get_students_age_groups():
    students = Student.objects.all()

    age_groups = {
        '0-12': 0,
        '13-17': 0,
        '18-30': 0,
        '31-50': 0,
        '51+': 0,
    }

    for student in students:
        age = student.age

        if age <= 12:
            age_groups['0-12'] += 1
        elif age <= 17:
            age_groups['13-17'] += 1
        elif age <= 30:
            age_groups['18-30'] += 1
        elif age <= 50:
            age_groups['31-50'] += 1
        else:
            age_groups['51+'] += 1

    return age_groups