from types import SimpleNamespace

from django.test import TestCase
from django.utils import timezone

from . import models

from nap import mapper, http
from nap.extras import actions


class ActionTestCase(TestCase):
    def test_smoke(self):
        poll = models.Poll.objects.create(question='Does this show?', pub_date=timezone.now())
        models.Choice.objects.create(poll=poll, choice_text='First Choice.')

        class M(mapper.ModelMapper):
            class Meta:
                model = models.Choice
                fields = '__all__'
                exclude = ('id',)

            @mapper.field
            def poll(self):
                return self.poll.question

            @mapper.field
            def votes(self):
                return str(self.votes)

        action = actions.ExportCsv(M)

        resp = action(SimpleNamespace(model=models.Choice), None, models.Choice.objects.all())
        output = resp.getvalue()
        for field in M._fields:
            self.assertTrue(field in output.decode('utf-8'))


class HttpTest(TestCase):
    def test_405(self):
        resp = http.MethodNotAllowed(['GET', 'POST'])
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp['Allow'], 'GET, POST')
