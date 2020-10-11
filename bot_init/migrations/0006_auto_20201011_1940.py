# Generated by Django 3.0.7 on 2020-10-11 16:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20201008_1529'),
        ('bot_init', '0005_auto_20201006_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='registry_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарй к подписчику'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='day',
            field=models.IntegerField(default=1, verbose_name='День'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='members_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='game.MembersGroup', verbose_name='Группа в которой состоит пользователь'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='step',
            field=models.CharField(max_length=1000, verbose_name='Шаг пользователя'),
        ),
    ]