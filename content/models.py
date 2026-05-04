from datetime import date

from django.db import models
from django.db.models import Q


class BannerQuerySet(models.QuerySet):
    def visible_today(self):
        """Banners that are active and within their validity window (if any)."""
        today = date.today()
        return self.filter(
            Q(status='active')
            & (Q(start_date__isnull=True) | Q(start_date__lte=today))
            & (Q(end_date__isnull=True) | Q(end_date__gte=today))
        )


class Banner(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(
        "Nome interno",
        max_length=100,
        help_text="Identificação interna do banner. Não aparece para o visitante.",
    )
    image = models.ImageField(
        "Imagem",
        upload_to='banners/',
        help_text="Imagem de fundo do banner. Recomendado pelo menos 1920x600 px.",
    )
    title = models.CharField(
        "Título",
        max_length=100,
        blank=True,
        help_text="Título principal do banner. Aparece em destaque sobre a imagem.",
    )
    subtitle = models.CharField(
        "Subtítulo",
        max_length=200,
        blank=True,
        help_text="Texto secundário do banner.",
    )
    link_url = models.URLField(
        "Link de destino",
        blank=True,
        help_text="URL para onde o banner leva quando clicado. Deixe vazio para banner não-clicável.",
    )
    link_label = models.CharField(
        "Texto do botão",
        max_length=40,
        blank=True,
        help_text="Texto do botão de ação (ex: 'SAIBA MAIS'). Só aparece se houver link.",
    )
    display_order = models.PositiveIntegerField(
        "Ordem de exibição",
        default=0,
        help_text="Posição na rotação do carrossel. Menor número aparece primeiro.",
    )
    start_date = models.DateField(
        "Início da exibição",
        null=True, blank=True,
        help_text="Data a partir da qual o banner começa a aparecer. Vazio = sempre.",
    )
    end_date = models.DateField(
        "Fim da exibição",
        null=True, blank=True,
        help_text="Data até quando o banner aparece. Vazio = sem expiração.",
    )
    status = models.CharField(
        "Status",
        max_length=10, choices=STATUS_CHOICES, default='active',
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    objects = BannerQuerySet.as_manager()

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ['display_order', '-created_at']

    def __str__(self) -> str:
        return self.name
