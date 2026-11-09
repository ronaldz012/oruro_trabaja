class DomainError(Exception):
    #Error de negocio esperado, con código estable para el cliente

    code = "DOMAIN_ERROR"
    status = 400

    def __init__(self, message: str, *, code: str | None = None, status: int | None = None):
        self.message = message
        self.code = code or self.code
        if status is not None:
            self.status = status
        super().__init__(message)


class Conflict(DomainError):
    status = 409


class NotFound(DomainError):
    status = 404


class Forbidden(DomainError):
    status = 403
