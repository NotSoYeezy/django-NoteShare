# Generated by Django 3.2 on 2021-07-04 14:40

from django.db import migrations
import notes.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0016_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=notes.fields.IntegerRangeField(),
        ),
    ]
