# Generated by Django 4.1.3 on 2022-11-14 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_orderitem_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='contact',
            field=models.CharField(default='', max_length=100),
        ),
    ]
