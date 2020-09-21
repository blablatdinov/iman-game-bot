# Generated by Django 3.0.7 on 2020-09-21 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot_init', '0004_auto_20200919_1735'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PointsRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_count', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_init.Subscriber')),
            ],
        ),
    ]
