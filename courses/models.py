from django.core.exceptions import ValidationError
from django.db import models

# Course #
class Course(models.Model):
    STATUS_CHOICES = [('active', 'Ativo'), ('inactive', 'Inativo')]

    name = models.CharField(
        "Nome",
        max_length=255,
    )
    description = models.TextField(
        "Descrição",
        help_text="Resumo curto do curso (1-2 parágrafos). Aparece em cards e topo da página de detalhes."
    )
    syllabus = models.TextField(
        "Roteiro",
        blank=True,
        help_text="Conteúdo programático do curso. Aceita Markdown (## títulos, - bullets, **negrito**)."
    )
    duration_hours = models.IntegerField(
        "Duração (horas)",
    )
    price = models.DecimalField(
        "Preço (R$)",
        max_digits=10, decimal_places=2,
    )
    status = models.CharField(
        "Status",
        max_length=10, choices=STATUS_CHOICES, default='active',
    )
    image = models.ImageField(
        "Imagem de capa",
        upload_to='courses/',
        blank=True, null=True,
        help_text="Imagem que aparece no card e na página de detalhes do curso."
    )
    min_age = models.PositiveIntegerField(
        "Idade mínima",
        null=True, blank=True,
        help_text="Idade mínima exigida para inscrição. Deixe vazio se não houver restrição."
    )
    has_certificate = models.BooleanField(
        "Emite certificado",
        default=True,
        help_text="O curso entrega certificado ao final?"
    )
    donation_kg_required = models.DecimalField(
        "Doação exigida (kg)",
        max_digits=6, decimal_places=2,
        null=True, blank=True,
        help_text="Quantos kg de ração são exigidos como parte do pagamento. Deixe vazio se não exigir doação."
    )
    instructors = models.ManyToManyField(
        'accounts.Instructor',
        verbose_name="Instrutores",
        related_name='courses',
        help_text="Instrutores que ministram este curso. Pelo menos 1."
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def clean(self):
        # M2M validation only runs after the initial save (pk must exist).
        # Django re-runs clean() in the admin after the M2M relations are persisted.
        if self.pk and not self.instructors.exists():
            raise ValidationError({"instructors": "O curso precisa ter pelo menos 1 instrutor."})

    def __str__(self) -> str:
        return str(self.name)

# Lesson
class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name='lessons',
        verbose_name="Curso",
    )
    start_date = models.DateField("Data")
    start_time = models.TimeField("Início")
    end_time = models.TimeField("Término")
    capacity = models.IntegerField("Capacidade")
    instructor = models.ForeignKey(
        'accounts.Instructor', on_delete=models.PROTECT, related_name='lessons',
        verbose_name="Instrutor",
    )
    label = models.CharField(
        "Nome da turma",
        max_length=100, blank=True,
        help_text="Nome opcional da turma (ex: 'Turma escola Eusébio Farias'). Se vazio, usa numeração automática."
    )
    is_private = models.BooleanField(
        "Turma fechada",
        default=False,
        help_text="Turma fechada: não aparece na listagem pública e só admin pode inscrever alunos."
    )

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self) -> str:
        suffix = self.label or str(self.start_date)
        return f"{self.course.name} - {suffix}"

