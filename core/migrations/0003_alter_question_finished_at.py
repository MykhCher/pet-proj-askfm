# Generated by Django 4.1 on 2022-08-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_answer_author_question_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='finished_at',
            field=models.DateTimeField(blank=True, default=False, null=True),
        ),
    ]
