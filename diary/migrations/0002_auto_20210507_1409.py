# Generated by Django 3.0.5 on 2021-05-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='write',
            name='board_emo',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='write',
            name='board_tag',
            field=models.CharField(max_length=20),
        ),
    ]