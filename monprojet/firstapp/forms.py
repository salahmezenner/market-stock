from django import forms
from .models import AchatDetails, Employee,VenteDetails,PayementAchat,PayementVente , Fournisseur , Client , Stock , TransferDetails, VenteDetails2
from .models import Massrouf , Abcense

class AchatDetailsForm(forms.ModelForm):
    class Meta:
        model = AchatDetails
        fields = ['stock', 'fournisseur', 'dateAchat', 'quantite','prixTotale']
        widgets = {
            'dateAchat': forms.DateInput(attrs={'type': 'date'}),
            'prixTotale': forms.HiddenInput(),
        }
        labels = {
            'stock': 'produit',
        }

class VenteDetailsForm(forms.ModelForm):
    class Meta:
        model = VenteDetails
        fields = ['stock', 'client', 'dateVente', 'quantite','prixTotale',]
        widgets = {
            'dateVente': forms.DateInput(attrs={'type': 'date'}),
            'prixTotale': forms.HiddenInput(),
        }
        labels = {
            'stock': 'produit',
        }

class PayementAchatForm(forms.ModelForm):
    class Meta:
        model = PayementAchat
        fields = ['fournisseur', 'montantPaye', 'datePayement',]
        widgets = {
            'datePayement': forms.DateInput(attrs={'type': 'date'}),
        }

class PayementVenteForm(forms.ModelForm):
    class Meta:
        model = PayementVente
        fields = ['client', 'montantPaye', 'datePayement',]
        widgets = {
            'datePayement': forms.DateInput(attrs={'type': 'date'}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['NomF', 'PrenomF', 'TelF', 'AdressF', 'SoldeF']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

class PayementAchatForm(forms.ModelForm):
    class Meta:
        model = PayementAchat
        fields = '__all__'

class PayementVenteForm(forms.ModelForm):
    class Meta:
        model = PayementVente
        fields = '__all__'

class TransferDetailsForm(forms.ModelForm):
    class Meta:
        model = TransferDetails
        fields = ['Stock','numC','date','quantite']

class EmployeeForm(forms.ModelForm):
    class Meta : 
        model = Employee 
        fields = '__all__'

class MasroufForm(forms.ModelForm):
    class Meta :
        model = Massrouf
        fields = '__all__'

class AbcenseForm(forms.ModelForm):
    class Meta : 
        model = Abcense
        fields = '__all__'

class VenteDetailsForm2(forms.ModelForm):
    class Meta:
        model = VenteDetails2
        fields = ['stockCentre', 'client', 'dateVente', 'quantite','prixTotale',]
        widgets = {
            'dateVente': forms.DateInput(attrs={'type': 'date'}),
            'prixTotale': forms.HiddenInput(),
        }
        labels = {
            'stockCentre': 'prd',
        }