from dataclasses import dataclass

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from apps.platform.accounts.models import Role, User
from core.exceptions import Conflict, DomainError


@dataclass(frozen=True)
class CrearUsuarioInput:
    email: str
    password: str | None = None
    password_hash: str | None = None
    role_code: str = Role.Code.POSTULANTE
    celular: str | None = None
    first_name: str = ""
    last_name: str = ""
    actor: User | None = None
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True
    celular_verificado: bool = False


class CrearUsuario:
    @transaction.atomic
    def execute(self, data: CrearUsuarioInput) -> User:
        email = data.email.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise Conflict(
                "Ya existe un usuario con ese email.",
                code="EMAIL_ALREADY_EXISTS",
            )

        try:
            role = Role.objects.get(codigo=data.role_code)
        except Role.DoesNotExist as exc:
            raise DomainError("Rol inválido.", code="ROLE_NOT_FOUND") from exc

        if data.password_hash:
            # La contraseña ya viene hasheada desde el registro pendiente.
            user = User(
                email=email,
                role=role,
                celular=data.celular or None,
                first_name=data.first_name,
                last_name=data.last_name,
                is_staff=data.is_staff,
                is_superuser=data.is_superuser,
                is_active=data.is_active,
                celular_verificado=data.celular_verificado,
            )
            user.password = data.password_hash
            user.save()
            return user

        if not data.password:
            raise DomainError("La contraseña es obligatoria.", code="PASSWORD_REQUIRED")

        try:
            validate_password(data.password)
        except DjangoValidationError as exc:
            raise DomainError(
                " ".join(exc.messages),
                code="WEAK_PASSWORD",
            ) from exc

        user = User.objects.create_user(
            email=email,
            password=data.password,
            celular=data.celular or None,
            role=role,
            first_name=data.first_name,
            last_name=data.last_name,
            is_staff=data.is_staff,
            is_superuser=data.is_superuser,
            is_active=data.is_active,
            celular_verificado=data.celular_verificado,
        )  # type: ignore
        return user
