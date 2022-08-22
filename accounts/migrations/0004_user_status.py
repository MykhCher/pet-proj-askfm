# Generated by Django 4.1 on 2022-08-22 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_managers_remove_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('a', 'Active'), ('b', 'Blocked')], default='a', max_length=1),
        ),
    ]
