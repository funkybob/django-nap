from types import SimpleNamespace

from django.test import TestCase

from . import models

from nap import mapper
from nap.extras import actions


class ActionTestCase(TestCase):
    def test_smoke(self):
        class M(mapper.ModelMapper):
            class Meta:
                model = models.Choice
                fields = '__all__'

        action = actions.ExportCsv(M)

        resp = action(SimpleNamespace(model=models.Choice), None, models.Choice.objects.all())
        output = resp.getvalue()
        # for field in M._fields:
        #     self.assertTrue(field in output)
