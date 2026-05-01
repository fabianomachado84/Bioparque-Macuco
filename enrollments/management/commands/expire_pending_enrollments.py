from django.core.management.base import BaseCommand
from django.utils import timezone

from enrollments.models import Enrollment


class Command(BaseCommand):
    help = (
        "Marca como 'expired' todas as inscrições pendentes cujo prazo "
        "(expires_at) já passou, liberando as vagas para outros alunos."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Apenas lista o que seria expirado, sem alterar o banco.",
        )

    def handle(self, *args, **options):
        now = timezone.now()
        qs = Enrollment.objects.filter(
            status="pending",
            expires_at__isnull=False,
            expires_at__lt=now,
        )
        count = qs.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS("Nenhuma inscrição pendente expirada."))
            return

        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"[dry-run] {count} inscrição(ões) seriam expiradas:")
            )
            for enrollment in qs:
                self.stdout.write(f"  - #{enrollment.id} {enrollment}")
            return

        updated = qs.update(status="expired")
        self.stdout.write(
            self.style.SUCCESS(f"{updated} inscrição(ões) expirada(s) com sucesso.")
        )
