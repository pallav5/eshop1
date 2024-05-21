# Generated by Django 3.2.19 on 2023-05-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopapp', '0003_auto_20230529_2041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productbrand',
            name='slug',
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, null=True, unique=True),
        ),
    ]
