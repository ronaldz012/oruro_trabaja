from django.core.management.base import BaseCommand, CommandError

from apps.platform.accounts.sms import get_sms_backend
from core.exceptions import DomainError


class Command(BaseCommand):
    help = "Envía un SMS de prueba usando el backend configurado."

    def add_arguments(self, parser):
        parser.add_argument(
            "celular",
            help="Número en formato E.164, por ejemplo +59171234567.",
        )

    def handle(self, *args, **options):
        celular = options["celular"]
        try:
            get_sms_backend().enviar(
                celular,
                "Oruro Trabaja: SMS de prueba. Si recibís este mensaje, "
                "el envío funciona.",
            )
        except DomainError as exc:
            raise CommandError(exc.message) from exc

        self.stdout.write(
            self.style.SUCCESS(f"SMS de prueba procesado para {celular}.")
        )
