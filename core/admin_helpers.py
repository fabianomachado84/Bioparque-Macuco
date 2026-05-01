"""Reusable building blocks for ModelAdmin classes."""

from django.db import models
from django.forms import widgets


class NativeDatePickerMixin:
    """Replace Django's default jQuery datepicker with the browser's native HTML5 picker.

    The native picker lets users click the month/year header to jump
    directly to any date, which is much faster for fields like birth
    dates than navigating month-by-month.

    Apply by adding it as the first base class:

        @admin.register(MyModel)
        class MyAdmin(NativeDatePickerMixin, admin.ModelAdmin):
            ...
    """

    formfield_overrides = {
        models.DateField: {
            "widget": widgets.DateInput(attrs={"type": "date"}),
        },
        models.DateTimeField: {
            "widget": widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        },
    }
