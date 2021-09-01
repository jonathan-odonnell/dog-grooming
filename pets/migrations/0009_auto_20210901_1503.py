# Generated by Django 3.2.5 on 2021-09-01 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0008_auto_20210901_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emergencycontact',
            options={'ordering': ('id',)},
        ),
        migrations.AlterField(
            model_name='vet',
            name='pet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vet', to='pets.pet'),
        ),
    ]
