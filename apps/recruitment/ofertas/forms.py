from __future__ import annotations

from django import forms
from django.utils import timezone

from apps.recruitment.catalogos.models import Habilidad
from apps.recruitment.ofertas.models import Oferta, OfertaHabilidad


class OfertaForm(forms.ModelForm):
    habilidades_obligatorias = forms.ModelMultipleChoiceField(
        label="Habilidades obligatorias",
        queryset=Habilidad.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "input min-h-36"}),
    )
    habilidades_deseables = forms.ModelMultipleChoiceField(
        label="Habilidades deseables",
        queryset=Habilidad.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "input min-h-36"}),
    )

    class Meta:
        model = Oferta
        fields = (
            "titulo",
            "descripcion",
            "requisitos_obligatorios",
            "requisitos_deseables",
            "profesiones",
            "anos_experiencia",
            "tipo_contrato",
            "modalidad",
            "departamento",
            "municipio",
            "salario_min",
            "salario_max",
            "a_tratar",
            "beneficios",
            "fecha_cierre",
            "plazas",
        )
        widgets = {  # noqa: RUF012
            "titulo": forms.TextInput(
                attrs={"class": "input", "placeholder": "Ej. Desarrollador Full Stack"}
            ),
            "descripcion": forms.Textarea(
                attrs={"class": "input min-h-28", "rows": 4}
            ),
            "requisitos_obligatorios": forms.Textarea(
                attrs={"class": "input min-h-24", "rows": 3}
            ),
            "requisitos_deseables": forms.Textarea(
                attrs={"class": "input min-h-24", "rows": 3}
            ),
            "profesiones": forms.SelectMultiple(
                attrs={"class": "input min-h-36"}
            ),
            "anos_experiencia": forms.NumberInput(
                attrs={"class": "input", "min": 0, "max": 60}
            ),
            "tipo_contrato": forms.Select(attrs={"class": "input"}),
            "modalidad": forms.Select(attrs={"class": "input"}),
            "departamento": forms.Select(attrs={"class": "input"}),
            "municipio": forms.TextInput(
                attrs={"class": "input", "placeholder": "Ej. Oruro"}
            ),
            "salario_min": forms.NumberInput(
                attrs={"class": "input", "min": 0, "step": "0.01"}
            ),
            "salario_max": forms.NumberInput(
                attrs={"class": "input", "min": 0, "step": "0.01"}
            ),
            "a_tratar": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 rounded border-secondary-300 text-primary-600 focus:ring-primary-300"
                }
            ),
            "beneficios": forms.Textarea(
                attrs={"class": "input min-h-24", "rows": 3}
            ),
            "fecha_cierre": forms.DateInput(
                attrs={"class": "input", "type": "date"}
            ),
            "plazas": forms.NumberInput(
                attrs={"class": "input", "min": 1, "max": 999}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profesiones"].label = "Profesiones afines (opcional)"
        self.fields["profesiones"].help_text = (
            "Se usa para afinidad y búsqueda; no bloquea postulaciones."
        )
        self.fields["profesiones"].required = False
        self.fields["habilidades_obligatorias"].help_text = (
            "Elegí habilidades de la lista y agregalas como tags."
        )
        self.fields["habilidades_deseables"].help_text = (
            "Opcional. Habilidades que suman pero no son obligatorias."
        )
        if self.instance and self.instance.pk:
            requisitos = self.instance.requerimientos_habilidad.select_related(
                "habilidad"
            )
            self.fields["habilidades_obligatorias"].initial = [
                r.habilidad_id for r in requisitos if r.obligatoria
            ]
            self.fields["habilidades_deseables"].initial = [
                r.habilidad_id for r in requisitos if not r.obligatoria
            ]

    def _seleccionadas(self, nombre: str) -> list[dict]:
        valores = {str(valor) for valor in (self[nombre].value() or [])}
        return [
            {"id": obj.pk, "nombre": str(obj)}
            for obj in self.fields[nombre].queryset
            if str(obj.pk) in valores
        ]

    @property
    def profesiones_seleccionadas(self):
        return self._seleccionadas("profesiones")

    @property
    def habilidades_obligatorias_seleccionadas(self):
        return self._seleccionadas("habilidades_obligatorias")

    @property
    def habilidades_deseables_seleccionadas(self):
        return self._seleccionadas("habilidades_deseables")

    def clean_fecha_cierre(self):
        fecha = self.cleaned_data["fecha_cierre"]
        if fecha < timezone.localdate():
            raise forms.ValidationError("La fecha de cierre no puede estar en el pasado.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        minimo = cleaned_data.get("salario_min")
        maximo = cleaned_data.get("salario_max")
        if minimo is not None and maximo is not None and minimo > maximo:
            self.add_error(
                "salario_max",
                "El salario máximo debe ser mayor o igual al mínimo.",
            )

        obligatorias = cleaned_data.get("habilidades_obligatorias")
        deseables = cleaned_data.get("habilidades_deseables")
        if obligatorias and deseables:
            repetidas = set(obligatorias) & set(deseables)
            if repetidas:
                self.add_error(
                    "habilidades_deseables",
                    "Una habilidad no puede ser obligatoria y deseable a la vez.",
                )
        return cleaned_data

    def save(self, commit=True):
        oferta = super().save(commit=commit)
        if not commit:
            return oferta

        if oferta.a_tratar:
            oferta.salario_min = None
            oferta.salario_max = None
            oferta.save(update_fields=["salario_min", "salario_max", "actualizado_en"])

        oferta.requerimientos_habilidad.all().delete()
        obligatorias = self.cleaned_data.get("habilidades_obligatorias") or []
        deseables = self.cleaned_data.get("habilidades_deseables") or []
        OfertaHabilidad.objects.bulk_create(
            [
                OfertaHabilidad(
                    oferta=oferta,
                    habilidad=habilidad,
                    obligatoria=True,
                )
                for habilidad in obligatorias
            ]
            + [
                OfertaHabilidad(
                    oferta=oferta,
                    habilidad=habilidad,
                    obligatoria=False,
                )
                for habilidad in deseables
            ]
        )
        return oferta
