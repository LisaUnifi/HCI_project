# Generated by Django 3.0.3 on 2022-02-18 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0014_auto_20220218_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='reparto',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]