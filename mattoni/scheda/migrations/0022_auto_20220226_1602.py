# Generated by Django 3.0.3 on 2022-02-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0021_auto_20220226_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='cognome_p',
            field=models.CharField(default='NON DEFINITO', max_length=20, null=True),
        ),
    ]