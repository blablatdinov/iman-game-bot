# Generated by Django 3.0.7 on 2020-11-18 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_dailytask_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytask',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='task_type',
            field=models.CharField(choices=[('body', 'тело'), ('soul', 'душа'), ('spirit', 'дух')], max_length=16, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='week_day',
            field=models.CharField(choices=[('mon', 'понедельник'), ('tue', 'вторник'), ('wed', 'среда'), ('thu', 'четверг'), ('fri', 'пятница'), ('sat', 'суббота'), ('sun', 'воскресенье')], max_length=5, verbose_name='День недели'),
        ),
    ]
