# Generated by Django 3.0.7 on 2020-10-06 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Навзвание')),
                ('text', models.TextField(verbose_name='Текст сообщения')),
                ('key', models.CharField(max_length=128, verbose_name='Ключ, по которому сообщение вызывается в коде')),
            ],
            options={
                'verbose_name': 'Админитративное сообщение',
                'verbose_name_plural': 'Админитративное сообщения',
            },
        ),
        migrations.AddField(
            model_name='message',
            name='is_removed',
            field=models.BooleanField(default=False, verbose_name='Удалено ли сообщение у пользователя'),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='day',
            field=models.IntegerField(default=1),
        ),
    ]
