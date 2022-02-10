# Generated by Django 3.0.3 on 2022-02-10 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0006_auto_20220210_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missione',
            name='arrivo',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='avvisi',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='cap_residenza',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='cellulare',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='missione',
            name='civico_residenza',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='missione',
            name='comune_residenza',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='missione',
            name='data_nascita',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='dove_nato',
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='missione',
            name='esito',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='missione',
            name='eta',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='fine',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='inizio',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='invio',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='nome_p',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='missione',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='partenza',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='pronto_socc',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='missione',
            name='provincia_residenza',
            field=models.CharField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='missione',
            name='residenza',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='missione',
            name='sede',
            field=models.DateTimeField(blank=True),
        ),
    ]
