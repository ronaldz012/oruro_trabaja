from __future__ import annotations

import json
import logging
from typing import Protocol
from urllib import error, request

from django.conf import settings

from core.exceptions import DomainError

logger = logging.getLogger(__name__)


class SmsBackend(Protocol):
    def enviar(self, celular: str, mensaje: str) -> None: ...


class DemoSmsBackend:
    """No envía SMS: deja el código en el log y la vista lo muestra en pantalla."""

    def enviar(self, celular: str, mensaje: str) -> None:
        logger.info("[DEMO] SMS a %s: %s", celular, mensaje)


class TextbeeSmsBackend:
    """Envía SMS reales mediante la API de Textbee."""

    def __init__(self):
        self.api_key = settings.TEXTBEE_API_KEY
        self.device_id = settings.TEXTBEE_DEVICE_ID
        self.base_url = settings.TEXTBEE_BASE_URL.rstrip("/")
        self.timeout = settings.TEXTBEE_TIMEOUT_SECONDS

    def enviar(self, celular: str, mensaje: str) -> None:
        if not self.api_key or not self.device_id:
            raise DomainError(
                "Textbee no está configurado. Revisá TEXTBEE_API_KEY y "
                "TEXTBEE_DEVICE_ID.",
                code="SMS_CONFIG",
            )

        payload = {
            "recipients": [celular],
            "message": mensaje,
            "deviceId": self.device_id,
        }
        solicitud = request.Request(
            f"{self.base_url}/gateway/send-sms",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            },
            method="POST",
        )

        try:
            with request.urlopen(solicitud, timeout=self.timeout) as respuesta:
                respuesta.read()
        except error.HTTPError as exc:
            logger.warning("Textbee respondió HTTP %s.", exc.code)
            raise DomainError(
                "No se pudo enviar el SMS. Intenta nuevamente.",
                code="SMS_ERROR",
            ) from exc
        except (error.URLError, TimeoutError) as exc:
            logger.warning("Textbee no respondió: %s.", exc)
            raise DomainError(
                "No se pudo enviar el SMS. Intenta nuevamente.",
                code="SMS_ERROR",
            ) from exc

        logger.info("Textbee: SMS encolado correctamente.")


def get_sms_backend() -> SmsBackend:
    if settings.DEMO_MODE:
        return DemoSmsBackend()
    return TextbeeSmsBackend()

