from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*codigos: str):
    #Exige que el usuario autenticado tenga uno de los roles indicados

    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            role = getattr(getattr(request.user, "role", None), "codigo", None)
            if role not in codigos:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
