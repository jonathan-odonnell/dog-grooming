# Generated by Django 3.2.5 on 2021-08-15 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0013_alter_price_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='price',
            old_name='size',
            new_name='dog_size',
        ),
    ]
