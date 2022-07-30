# Generated by Django 3.2.14 on 2022-07-30 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot_db', '0002_auto_20220727_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('top_block', models.CharField(max_length=255)),
                ('bottom_block', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.RenameField(
            model_name='speaker',
            old_name='speech_theme',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='speaker',
            name='name',
        ),
        migrations.RemoveField(
            model_name='speaker',
            name='speech_begin_time',
        ),
        migrations.RemoveField(
            model_name='speaker',
            name='speech_end_time',
        ),
    ]