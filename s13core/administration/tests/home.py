from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse


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

    def test_form_macros(self):
        response = self.c.get(reverse('s13admin:login'))
        content = str(response.content)
        # These attributes have been supplied by macros in form_macros.html
        self.assertIn('id="id_username"', content)
        self.assertIn('name="csrfmiddlewaretoken"', content)
        self.assertIn('value="Log In"', content)

    def test_login(self):
        # Get to the login form.
        response = self.c.get(reverse('s13admin:login'))
        self.assertEqual(response.status_code, 200)
        # Post invalid login credentials.
        response = self.c.post(
            reverse('s13admin:login'),
            {'username': 'invalid-username', 'password': 'invalid-password'}
        )
        self.assertEqual(response.status_code, 200)
        # Post valid login credentials.
        response = self.c.post(
            reverse('s13admin:login'),
            {'username': 'username', 'password': 'password'}
        )
        self.assertRedirects(response, reverse('s13admin:dashboard'))

    def test_logout(self):
        self.c.login(username='username', password='password')
        response = self.c.get(reverse('s13admin:logout'), follow=True)
        self.assertRedirects(response, reverse('s13admin:login'))
        self.assertIn('Goodbye', str(response.content))

    def test_admin_home_login_required(self):
        response = self.c.get(reverse('s13admin:dashboard'))
        self.assertRedirects(response, reverse('s13admin:login'))
        # Log the client in.
        self.c.login(username='username', password='password')
        response = self.c.get(reverse('s13admin:dashboard'))
        self.assertIn('Dashboard</title>', str(response.content))

    def test_update_user_info(self):
        # Load the user so we can get its pk.
        user = User.objects.get(username='username')
        # New info to save.
        first_name = 'Juan'
        last_name = 'de la Cruz'
        self.c.login(username='username', password='password')
        response = self.c.post(
            reverse('s13admin:update_user_info', args=[user.pk]),
            {'first_name': first_name, 'last_name': last_name},
            follow=True  # Because this redirects.
        )
        self.assertRedirects(response, reverse('s13admin:dashboard'))
        self.assertIn('User information changed.', str(response.content))
        # Reload the user so we can test if it was edited.
        user = User.objects.get(username='username')
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_update_password(self):
        user = User.objects.all()[0]
        new_password = 'new-password'
        self.c.login(username='username', password='password')
        # These redirect to the new dashboard because there is a
        # mismatch betweeen the current, new_ and confirm_ passwords.
        response = self.c.post(
            reverse('s13admin:update_password', args=[user.pk]),
            {'password': 'password-invalid',
             'new_password': new_password,
             'confirm_password': new_password},
            follow=True
        )
        self.assertIn('Invalid current password.', str(response.content))
        response = self.c.post(
            reverse('s13admin:update_password', args=[user.pk]),
            {'password': 'password',
             'new_password': new_password,
             'confirm_password': 'not-the-password'},
            follow=True
        )
        self.assertIn(
            'New and confirm password mismatch.', str(response.content))
        # This will succeed and therefore, will redirect to the login page.
        response = self.c.post(
            reverse('s13admin:update_password', args=[user.pk]),
            {'password': 'password',
             'new_password': new_password,
             'confirm_password': new_password},
            follow=True
        )
        self.assertRedirects(response, reverse('s13admin:login'))
        logged_in = self.c.login(username='username', password=new_password)
        self.assertTrue(logged_in)
