# Generated by Django 3.0.7 on 2020-09-26 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_recorddailytask_is_selected'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordDailyTaskGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='recorddailytask',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='game.RecordDailyTaskGroup'),
            preserve_default=False,
        ),
    ]