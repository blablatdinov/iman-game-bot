# Generated by Django 3.0.7 on 2020-09-26 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0006_adminmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='day',
            field=models.IntegerField(default=1),
        ),
    ]