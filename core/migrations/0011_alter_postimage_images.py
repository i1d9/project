# Generated by Django 4.1.3 on 2022-11-14 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_delete_likepost_alter_postimage_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='images',
            field=models.ImageField(default='', upload_to='post_images'),
        ),
    ]
