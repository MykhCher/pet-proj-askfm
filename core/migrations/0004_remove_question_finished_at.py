# Generated by Django 4.1 on 2022-08-14 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_question_finished_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='finished_at',
        ),
    ]
