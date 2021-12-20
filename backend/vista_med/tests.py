from django.test import TestCase


class WorkingWithVistaMedDatabaseTestCase(TestCase):
    def setUp(self):
        from inspect import isclass

        from django.db.models import Model

        from . import models

        self.models = []
        for obj in models.__dict__.values():
            if isclass(obj) and issubclass(obj, Model) and not obj._meta.abstract:
                self.models.append(obj)

    def test_all_models_unmanaged(self):
        for model in self.models:
            self.assertFalse(model._meta.managed, msg=f"{model} model must not be managed")

    def test_all_models_read_only(self):
        for model in self.models:
            with self.assertRaisesRegexp(
                RuntimeError, r"models of \w+ app are read-only", msg=f"{model} model must be read-only"
            ):
                model.objects.create()
