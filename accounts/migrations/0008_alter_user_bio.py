# Generated by Django 3.2 on 2021-05-06 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20210506_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, max_length=600),
        ),
    ]