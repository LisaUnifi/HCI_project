# Generated by Django 3.0.3 on 2022-02-18 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0011_auto_20220217_2255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='missione',
            old_name='cognome_s',
            new_name='parentela',
        ),
        migrations.RemoveField(
            model_name='missione',
            name='nome_s',
        ),
        migrations.AlterField(
            model_name='missione',
            name='esito',
            field=models.BooleanField(default=True),
        ),
    ]
