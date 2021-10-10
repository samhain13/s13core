from django.core.validators import validate_email
from django.db import models


TEXT_TO_LIST_SEPARATOR = ' -+|+- '


class QuestionAnswerPair(models.Model):
    '''Question-answer pairs serve as part of our anti-spam protection.
    Basically, contact/message forms are to have a hidden field for a
    randomly picked question and the user has to provide an acceptable
    answer.
    '''
    question = models.CharField(max_length=128)
    answer = models.TextField()

    class Meta:
        verbose_name = 'question-anwser pair'
        verbose_name_plural = 'question-answer pairs'

    def check_answer(self, answer):
        return answer.strip().lower() in self.get_answers()

    def get_answers(self):
        return self.answer.split(TEXT_TO_LIST_SEPARATOR)

    def save_answers(self, answers_list):
        if type(answers_list) in [list, tuple]:
            self.answer = TEXT_TO_LIST_SEPARATOR.join(answers_list).lower()


class SiteMessage(models.Model):
    '''SiteMessage objects are messages sent by public users to administrators
    via a contact form.
    '''
    sender_name = models.CharField(max_length=128)
    sender_email = models.EmailField(validators=[validate_email])
    message_body = models.TextField()
    date_sent = models.DateTimeField(auto_now=True)
    is_sent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
