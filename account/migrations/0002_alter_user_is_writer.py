# Generated by Django 5.0.6 on 2024-09-07 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_writer',
            field=models.BooleanField(default=False, verbose_name='Je suis Editeur'),
        ),
    ]
