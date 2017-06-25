from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from s13core.settings.models import Setting


class HttpTests(TestCase):
    c = Client()

    def setUp(self):
        # Create a user if we do not have one.
        if User.objects.count() < 1:
            User.objects.create_user(
                username='username', password='password', email='user@site.com'
            )
        # Reset the user to its original state.
        else:
            u = User.objects.get(pk=1)
            u.username = 'username'
            u.email = 'user@site.com'
            u.set_password('password')
            u.save()

    def test_settings_list(self):
        response = self.c.get(reverse('s13admin:settings'))
        self.assertEqual(response.status_code, 302)
        # The view requires that we login.
        self.c.login(username='username', password='password')
        response = self.c.get(reverse('s13admin:settings'))
        self.assertEqual(response.status_code, 200)

    def test_settings_crud(self):
        self.c.login(username='username', password='password')
        # Create settings.
        response = self.c.post(
            reverse('s13admin:create_settings'),
            {'name': 'My Settings',
             'title': 'My S13Core Website',
             'nohome_content_items': 1
            }
        )
        settings = Setting.objects.get(name='My Settings')
        self.assertTrue(settings.is_active)  # Automatically set.
        # Retrieve.
        response = self.c.get(reverse('s13admin:settings'))
        self.assertIn('<dd>My Settings</dd>', str(response.content))
        # Update.
        response = self.c.post(
            reverse('s13admin:update_settings', args=[settings.pk]),
            {'name': 'My Updated Settings',
             'title': 'My New Title',
             'nohome_content_items': settings.nohome_content_items
            }
        )
        settings = Setting.objects.get(name='My Updated Settings')
        self.assertEqual(settings.title, 'My New Title')
        # Delete. Requires that we have two or more settings.
        Setting(name='Buffer Setting').save()
        response = self.c.post(
            reverse('s13admin:delete_settings', args=[settings.pk])
        )
        self.assertEqual(Setting.objects.count(), 1)
        settings = Setting.objects.get(name='Buffer Setting')
        self.assertTrue(settings.is_active)
