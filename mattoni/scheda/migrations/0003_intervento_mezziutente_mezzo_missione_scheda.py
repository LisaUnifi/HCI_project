# Generated by Django 3.0.3 on 2022-02-02 11:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0002_auto_20220121_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mezzo',
            fields=[
                ('id_mezzo', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=10, unique=True)),
                ('tipologia', models.CharField(max_length=10)),
                ('all_day', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Missione',
            fields=[
                ('id_missione', models.AutoField(primary_key=True, serialize=False)),
                ('luogo', models.CharField(max_length=1)),
                ('patologia', models.IntegerField()),
                ('criticita', models.CharField(max_length=1)),
                ('nome_p', models.CharField(max_length=20)),
                ('cognome_p', models.CharField(default='NON DEFINITO', max_length=20)),
                ('luogo_intervento', models.CharField(max_length=100)),
                ('comune_intervento', models.CharField(max_length=20)),
                ('residenza', models.CharField(max_length=100)),
                ('comune_residenza', models.CharField(max_length=20)),
                ('cellulare', models.CharField(max_length=15)),
                ('data_nascita', models.DateField()),
                ('dove_nato', models.CharField(max_length=25)),
                ('eta', models.IntegerField()),
                ('note', models.TextField()),
                ('avvisi', models.TextField()),
                ('invio', models.DateTimeField()),
                ('inizio', models.DateTimeField()),
                ('arrivo', models.DateTimeField()),
                ('partenza', models.DateTimeField()),
                ('pronto_socc', models.DateTimeField()),
                ('fine', models.DateTimeField()),
                ('sede', models.DateTimeField()),
                ('esito', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Scheda',
            fields=[
                ('id_scheda', models.AutoField(primary_key=True, serialize=False)),
                ('scenario', models.CharField(max_length=20)),
                ('cosciente', models.BooleanField()),
                ('respiraBLS', models.BooleanField()),
                ('circoloBLS', models.BooleanField()),
                ('dae', models.BooleanField()),
                ('cicli', models.IntegerField(default=0)),
                ('noteBLS', models.TextField()),
                ('pervieta', models.BooleanField()),
                ('ostruzione', models.BooleanField()),
                ('dispnea', models.BooleanField()),
                ('osservo', models.CharField(max_length=20)),
                ('palpo', models.CharField(max_length=20)),
                ('ascolto', models.BooleanField()),
                ('conto', models.IntegerField()),
                ('saturazione', models.IntegerField()),
                ('saturazione_oss', models.IntegerField()),
                ('ossigeno', models.IntegerField()),
                ('pressione_massima', models.IntegerField()),
                ('pressione_minima', models.IntegerField()),
                ('temperatura', models.IntegerField()),
                ('emorragie', models.CharField(max_length=20)),
                ('polso', models.BooleanField()),
                ('regolare_polso', models.BooleanField()),
                ('cute', models.CharField(max_length=20)),
                ('sudato', models.BooleanField()),
                ('dolore_toracico', models.BooleanField()),
                ('ora_dolore', models.DateTimeField()),
                ('tipo_dolore', models.BooleanField()),
                ('avpu', models.CharField(max_length=1)),
                ('tempo', models.BooleanField()),
                ('spazio', models.BooleanField()),
                ('mimica_c', models.CharField(max_length=10)),
                ('braccia_c', models.CharField(max_length=10)),
                ('linguaggio_c', models.BooleanField()),
                ('forza_sup', models.CharField(max_length=10)),
                ('forza_inf', models.CharField(max_length=10)),
                ('sens_sup', models.CharField(max_length=10)),
                ('sens_inf', models.CharField(max_length=10)),
                ('posizione', models.CharField(max_length=20)),
                ('allergie', models.TextField()),
                ('patologie', models.TextField()),
                ('glicemia', models.IntegerField()),
                ('farmaci', models.TextField()),
                ('pasto', models.TextField()),
                ('testa_piedi_front', models.ImageField(upload_to='')),
                ('testa_piedi_back', models.ImageField(upload_to='')),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MezziUtente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_mezzo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheda.Mezzo')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Intervento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_mezzo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheda.Mezzo')),
                ('id_missione', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheda.Missione')),
                ('id_scheda', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheda.Scheda')),
            ],
        ),
    ]
