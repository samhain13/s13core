from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from .models import Setting


class SettingsTests(TestCase):

    def test_must_always_have_one_setting(self):
        for x in range(4):
            Setting(name='Settings {}'.format(x), is_active=True).save()
        self.assertEqual(Setting.objects.count(), 4)
        for x in range(4):
            s = Setting.objects.get(name='Settings {}'.format(x))
            if x < 3:
                s.delete()
            else:
                self.assertRaises(ValidationError, s.delete)
        self.assertEqual(Setting.objects.count(), 1)
        self.assertTrue(Setting.objects.all()[0].is_active)

    def test_settings_name_unique(self):
        Setting(name='Settings Name', is_active=True).save()
        s = Setting(name='Settings Name')
        self.assertRaises(IntegrityError, s.save)
