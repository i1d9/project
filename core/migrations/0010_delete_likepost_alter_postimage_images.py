# Generated by Django 4.1.3 on 2022-11-14 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_orderitem_ordered_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LikePost',
        ),
        migrations.AlterField(
            model_name='postimage',
            name='images',
            field=models.FileField(upload_to='$<django.db.models.fields.related.ForeignKey>/post_images'),
        ),
    ]
