# Generated by Django 3.0.7 on 2020-09-26 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_pointsrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_type', models.CharField(choices=[('body', 'тело'), ('soul', 'душа'), ('spirit', 'дух')], max_length=16)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Задание для участников',
                'verbose_name_plural': 'Задания для участников',
            },
        ),
    ]
