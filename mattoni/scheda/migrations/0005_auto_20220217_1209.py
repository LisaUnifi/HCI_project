# Generated by Django 3.0.3 on 2022-02-17 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0004_auto_20220217_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheda',
            name='data_dolore',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scheda',
            name='ora_dolore',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
