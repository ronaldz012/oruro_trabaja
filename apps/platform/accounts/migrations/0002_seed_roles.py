from django.db import migrations

ROLES = [
    ("SUPERADMIN", "SuperAdmin GADOR"),
    ("EMPRESA", "Empresa"),
    ("POSTULANTE", "Postulante"),
]


def seed_roles(apps, schema_editor):
    Role = apps.get_model("accounts", "Role")
    for codigo, nombre in ROLES:
        Role.objects.get_or_create(
            codigo=codigo,
            defaults={"nombre": nombre},
        )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_roles, migrations.RunPython.noop),
    ]