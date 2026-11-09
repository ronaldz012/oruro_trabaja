from __future__ import annotations

from django.core.paginator import Paginator


def paginar(request, queryset, per_page: int):
    """Devuelve un Page de Django usando ?page= de la request."""
    return Paginator(queryset, per_page).get_page(request.GET.get("page"))
