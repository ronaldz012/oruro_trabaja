from django.core.files.storage import FileSystemStorage
from django.test import TestCase

from apps.recruitment.postulantes.models import PostulanteProfile
from core.storage import private_storage


class StorageTests(TestCase):
    def test_cv_uses_configured_private_storage(self):
        field = PostulanteProfile._meta.get_field("cv")

        self.assertIs(field.storage, private_storage())
        self.assertIsInstance(field.storage, FileSystemStorage)
