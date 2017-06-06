# from types import SimpleNamespace

from django.test import TestCase
# from django.core.exceptions import ValidationError

from nap.mapper import ModelMapper, field, Field

from . import models


class ModelMapperTestCase(TestCase):

    def test_basics(self):

        with self.assertRaises(RuntimeError):
            class M(ModelMapper):
                pass

        with self.assertRaises(ValueError):
            class M(ModelMapper):
                class Meta:
                    pass

    def test_safe_default(self):

        class M(ModelMapper):
            class Meta:
                model = models.Choice

        self.assertFalse(M._fields)

    def test_include_all(self):
        class M(ModelMapper):
            class Meta:
                model = models.Choice
                fields = '__all__'

        self.assertTrue('poll' in M._fields)
        self.assertTrue('choice_text' in M._fields)
        self.assertTrue('votes' in M._fields)

    def test_exclude_field(self):
        class M(ModelMapper):
            class Meta:
                model = models.Choice
                fields = '__all__'
                exclude = ('votes',)

        self.assertTrue('poll' in M._fields)
        self.assertTrue('choice_text' in M._fields)
        self.assertFalse('votes' in M._fields)

    def test_mask_field(self):
        class M(ModelMapper):
            class Meta:
                model = models.Choice
                fields = '__all__'

            @field
            def votes(self):
                return self.votes

        self.assertTrue('poll' in M._fields)
        self.assertTrue('choice_text' in M._fields)
        self.assertTrue('votes' in M._fields)
        self.assertFalse(isinstance(M._fields['votes'], Field))
