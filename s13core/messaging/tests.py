from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.test import Client
from django.test import TestCase

from s13core.settings.models import Setting

from .models import QuestionAnswerPair
from .models import SiteMessage


c = Client()


class MessagingTests(TestCase):

    def setUp(self):
        # We need settings.
        if Setting.objects.count() < 1:
            setting = Setting()
            setting.is_active = True
            setting.save()

    def test_make_message(self):
        msg = SiteMessage()
        msg.sender_email = 'hello, not an email.'
        self.assertRaises(ValidationError, msg.save)
        msg.sender_email = 'sender@example.com'
        msg.sender_name = 'anonymous'
        msg.message_body = 'Hello, world.'
        msg.save()
        self.assertEqual(msg.date_sent.date(), timezone.now().date())

    def test_make_question_answer_pair(self):
        # Q-A pairs serve as part of our anti-spam protection.
        qa = QuestionAnswerPair()
        qa.question = 'What is the capital of the Philippines?'
        qa.save_answers(['Manila', 'Maynila', 'Metro Manila', 'NCR'])
        qa.save()
        # 3 because we added 2 questions on migrate.
        self.assertEqual(QuestionAnswerPair.objects.count(), 3)
        # Test the answer checker.
        self.assertTrue(qa.check_answer('Manila'))
        self.assertTrue(qa.check_answer(' Maynila '))
        self.assertFalse(qa.check_answer('National Capital Region'))

    def test_access_sitemessage_page(self):
        response = c.get(reverse('s13messaging:sitemessage-form'))
        self.assertEqual(response.status_code, 200)
        # Because we have no data, the system messages should be present.
        response = c.post(reverse('s13messaging:sitemessage-form'), {})
        content = str(response.content)
        self.assertIn('id="system-messages"', content)
        
