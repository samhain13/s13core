# Generated by Django 3.2.8 on 2021-10-10 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_questionanswerpair'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionanswerpair',
            options={'verbose_name': 'question-anwser pair', 'verbose_name_plural': 'question-answer pairs'},
        ),
    ]
