# Generated by Django 3.0.3 on 2022-02-03 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheda', '0003_intervento_mezziutente_mezzo_missione_scheda'),
    ]

    operations = [
        migrations.AddField(
            model_name='mezzo',
            name='username',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MezziUtente',
        ),
    ]