# Generated by Django 4.1.3 on 2022-11-13 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_business',
            field=models.BooleanField(default=False),
        ),
    ]
