# Generated by Django 3.0.3 on 2022-03-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExifImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('album', models.CharField(blank=True, max_length=20, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='exif/')),
            ],
        ),
    ]
