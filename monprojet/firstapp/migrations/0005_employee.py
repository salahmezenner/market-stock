# Generated by Django 5.0.1 on 2024-01-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0004_remove_transferdetails_prixvente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=25)),
                ('prenom', models.CharField(max_length=25)),
                ('adresse', models.CharField(max_length=50)),
                ('telephone', models.PositiveIntegerField(unique=True)),
            ],
        ),
    ]
