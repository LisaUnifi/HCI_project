# Generated by Django 3.0.3 on 2022-02-17 21:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0009_auto_20220217_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='invio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]