from datetime import datetime
from django.db import models
from django.db.models import Sum

class Fournisseur (models.Model):
    codeF = models.AutoField(primary_key=True)
    NomF = models.CharField(max_length=25)
    PrenomF = models.CharField(max_length=25)
    TelF = models.IntegerField(unique=True)
    AdressF = models.CharField(max_length=50)
    SoldeF = models.DecimalField(max_digits=10 , decimal_places=2)
    def __str__(self):
        return self.NomF

class Client (models.Model):
    codeC = models.AutoField(primary_key=True)
    NomC = models.CharField(max_length=25)
    PrenomC = models.CharField(max_length=25)
    TelC = models.IntegerField(unique=True)
    AdressC = models.CharField(max_length=50)
    SoldeC = models.DecimalField(max_digits=10 , decimal_places=2)
    def __str__(self):
        return self.NomC

class Stock(models.Model):
    CodeP = models.AutoField(primary_key=True)
    NomP = models.CharField(max_length=25)
    quantite = models.IntegerField(default=0)
    prixUnitaire=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    prixVente=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    Designation = models.TextField(default='')
    def __str__(self):
        return self.NomP


class AchatDetails(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE,null=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE,null=True)
    dateAchat = models.DateField(null=True)
    quantite = models.IntegerField(null=True)
    prixTotale = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.stock.NomP} - {self.fournisseur.NomF} - {self.dateAchat} - {self.id} - {self.prixTotale}"
    
class VenteDetails(models.Model):
    id = models.AutoField(primary_key=True)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE,null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE,null=True)
    dateVente = models.DateField(null=True)
    quantite = models.IntegerField(null=True)
    prixTotale = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.stock.NomP} - {self.client.NomC} - {self.dateVente} - {self.id} - {self.prixTotale}"
    
class VenteDetails2(models.Model):
    id = models.AutoField(primary_key=True)
    stockCentre = models.ForeignKey('StockCentre', on_delete=models.CASCADE,null=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE,null=True)
    dateVente = models.DateField(null=True)
    quantite = models.IntegerField(null=True)
    prixTotale = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.StockCentre.NomP} - {self.client.NomC} - {self.dateVente} - {self.id} - {self.prixTotale}"
    
class PayementAchat(models.Model):
    id = models.AutoField(primary_key=True)
    fournisseur = models.ForeignKey('Fournisseur',on_delete=models.CASCADE,null=True)
    montantPaye = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    datePayement=models.DateField(null=True)
    def __str__(self):
        return f"{self.fournisseur} - {self.montantPaye} - {self.datePayement}"
    
class PayementVente(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client',on_delete=models.CASCADE,null=True)
    montantPaye = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    datePayement=models.DateField(null=True)
    def __str__(self):
        return f"{self.client} - {self.montantPaye} - {self.datePayement}"
         
class StockCentre(models.Model):
    id=models.AutoField(primary_key=True)
    nomP=models.CharField(max_length=25)
    quantite = models.IntegerField(default=0)
    numC = models.IntegerField(default=0)
    prixVente=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    Designation = models.TextField(default='')
    def __str__(self):
        return f"{self.nomP}-{self.numC}"
    
class TransferDetails(models.Model):
    id=models.AutoField(primary_key=True)
    Stock= models.ForeignKey('Stock', on_delete=models.CASCADE,null=True)
    numC = models.IntegerField(default=0)
    date=models.DateField(null=True)
    quantite = models.IntegerField(default=0)
    cout = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.numC}-{self.Stock.NomP}"
    
class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    nom=models.CharField(max_length=25)
    prenom=models.CharField(max_length=25)
    adresse=models.CharField(max_length=50)
    telephone=models.PositiveIntegerField(unique=True)
    salairejour=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    numC=models.PositiveBigIntegerField()
    salaire_mois=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    def __str__(self):
        return f"{self.nom}-{self.prenom}"
    def salaire_mois(self):
        current_month = datetime.now().month
        current_year = datetime.now().year

        somme_massrouf = Massrouf.objects.filter(
            employee=self, date__month=current_month, date__year=current_year
        ).aggregate(total_massrouf=Sum('somme'))['total_massrouf'] or 0

        somme_absence = Abcense.objects.filter(
            employee=self, date__month=current_month, date__year=current_year
        ).count()

        salaire_mois = self.salairejour * 26 - somme_massrouf - self.salairejour * somme_absence
        return salaire_mois
    def __str__(self):
        return f"{self.nom}-{self.prenom}"

class Massrouf(models.Model):
    id=models.AutoField(primary_key=True)
    employee=models.ForeignKey('Employee', on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    somme=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    class Meta : 
        unique_together =['employee','date']
    def __str__(self):
        return f"{self.employee}-{self.date}-{self.somme}"
    
class Abcense(models.Model):
    id=models.AutoField(primary_key=True)
    employee=models.ForeignKey('Employee', on_delete=models.CASCADE,null=True)
    date=models.DateField(null=True)
    class Meta:
        unique_together =['employee','date']