# Generated by Django 3.2.19 on 2024-03-28 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopapp', '0010_auto_20230603_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='color',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='size',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
