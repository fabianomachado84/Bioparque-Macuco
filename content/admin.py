from django.contrib import admin
from django.utils.html import format_html

from core.admin_helpers import NativeDatePickerMixin

from .models import Banner


@admin.register(Banner)
class BannerAdmin(NativeDatePickerMixin, admin.ModelAdmin):
    list_display = ['preview', 'name', 'title', 'display_order', 'status', 'is_visible_now']
    list_display_links = ['preview', 'name']
    list_filter = ['status']
    search_fields = ['name', 'title', 'subtitle']
    ordering = ['display_order', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['display_order', 'status']
    fieldsets = (
        ('Identificação', {
            'fields': ('name', 'status'),
            'description': 'O nome interno só aparece aqui no admin, ajuda você a achar o banner depois.',
        }),
        ('Conteúdo visível', {
            'fields': ('image', 'title', 'subtitle'),
        }),
        ('Ação (opcional)', {
            'fields': ('link_url', 'link_label'),
            'description': 'Se preencher o link, o banner inteiro fica clicável e (opcionalmente) mostra um botão.',
        }),
        ('Agendamento', {
            'fields': ('display_order', 'start_date', 'end_date'),
            'description': 'A ordem define a sequência de exibição. As datas são opcionais — vazio significa "sempre".',
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description="Pré-visualização")
    def preview(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" style="height: 50px; border-radius: 4px;" />',
            obj.image.url,
        )

    @admin.display(boolean=True, description="Visível hoje?")
    def is_visible_now(self, obj):
        return Banner.objects.visible_today().filter(pk=obj.pk).exists()
