# Generated by Django 3.2 on 2021-08-04 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='created_date',
            field=models.DateField(null=True),
        ),
    ]
