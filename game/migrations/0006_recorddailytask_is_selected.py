# Generated by Django 3.0.7 on 2020-09-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_recorddailytask'),
    ]

    operations = [
        migrations.AddField(
            model_name='recorddailytask',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
