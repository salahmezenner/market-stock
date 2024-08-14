# Generated by Django 5.0.1 on 2024-01-23 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('codeC', models.AutoField(primary_key=True, serialize=False)),
                ('NomC', models.CharField(max_length=25)),
                ('PrenomC', models.CharField(max_length=25)),
                ('TelC', models.IntegerField(unique=True)),
                ('AdressC', models.CharField(max_length=50)),
                ('SoldeC', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('codeF', models.AutoField(primary_key=True, serialize=False)),
                ('NomF', models.CharField(max_length=25)),
                ('PrenomF', models.CharField(max_length=25)),
                ('TelF', models.IntegerField(unique=True)),
                ('AdressF', models.CharField(max_length=50)),
                ('SoldeF', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('CodeP', models.AutoField(primary_key=True, serialize=False)),
                ('NomP', models.CharField(max_length=25)),
                ('quantite', models.IntegerField(default=0)),
                ('prixUnitaire', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prixVente', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('Designation', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='StockCentre',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nomP', models.CharField(max_length=25)),
                ('quantite', models.IntegerField(default=0)),
                ('numC', models.IntegerField(default=0)),
                ('prixVente', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('Designation', models.TextField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='PayementAchat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('montantPaye', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('datePayement', models.DateField(null=True)),
                ('fournisseur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.fournisseur')),
            ],
        ),
        migrations.CreateModel(
            name='PayementVente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('montantPaye', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('datePayement', models.DateField(null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.client')),
            ],
        ),
        migrations.CreateModel(
            name='AchatDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateAchat', models.DateField(null=True)),
                ('quantite', models.IntegerField(null=True)),
                ('prixTotale', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fournisseur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.fournisseur')),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.stock')),
            ],
        ),
        migrations.CreateModel(
            name='VenteDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateVente', models.DateField(null=True)),
                ('quantite', models.IntegerField(null=True)),
                ('prixTotale', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.client')),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='firstapp.stock')),
            ],
        ),
    ]
