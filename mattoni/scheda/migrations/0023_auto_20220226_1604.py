# Generated by Django 3.0.3 on 2022-02-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0022_auto_20220226_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='cognome_p',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
