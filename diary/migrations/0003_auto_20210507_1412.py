# Generated by Django 3.0.5 on 2021-05-07 05:12

from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20210507_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='write',
            name='board_emo',
            field=djongo.models.fields.JSONField(max_length=20),
        ),
        migrations.AlterField(
            model_name='write',
            name='board_tag',
            field=djongo.models.fields.JSONField(max_length=20),
        ),
    ]
