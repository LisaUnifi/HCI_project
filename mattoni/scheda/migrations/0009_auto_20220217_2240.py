# Generated by Django 3.0.3 on 2022-02-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0008_auto_20220217_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='invio',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
