# Generated by Django 4.1.7 on 2023-02-28 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
