# Generated by Django 3.0.3 on 2022-02-16 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheda',
            name='osservo',
        ),
        migrations.AddField(
            model_name='scheda',
            name='respira',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]