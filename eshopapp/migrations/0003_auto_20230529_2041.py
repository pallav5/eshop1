# Generated by Django 3.2.19 on 2023-05-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshopapp', '0002_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='productbrand',
            name='slug',
            field=models.SlugField(blank=True, editable=False, max_length=100, null=True, unique=True),
        ),
    ]
