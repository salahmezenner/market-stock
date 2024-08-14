from datetime import datetime
from django.shortcuts import render , get_object_or_404 , redirect
from django.db.models import Sum
import json
from django.http import Http404
from django.views import View
from .forms import MasroufForm , AbcenseForm, VenteDetailsForm2
from .forms import EmployeeForm, TransferDetailsForm ,AchatDetailsForm, VenteDetailsForm, PayementAchatForm, PayementVenteForm  , FournisseurForm , ClientForm , StockForm
from .models import Employee, Massrouf,TransferDetails,StockCentre,Fournisseur , Client , Stock , AchatDetails , VenteDetails , PayementAchat, PayementVente
from decimal import Decimal
from django.db.models.functions import ExtractMonth, ExtractYear
from django.core.serializers.json import DjangoJSONEncoder


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def achat(request):
    prix_totale = 0

    if request.method == 'POST':
        achat_form = AchatDetailsForm(request.POST, prefix='achat')
        if 'calculer_achat' in request.POST:
            if achat_form.is_valid():
                stock = achat_form.cleaned_data['stock']
                quantite = achat_form.cleaned_data['quantite']
                prix_unitaire = stock.prixUnitaire
                prix_totale = quantite * prix_unitaire

        elif 'acheter' in request.POST:
            if achat_form.is_valid():
                stock = achat_form.cleaned_data['stock']
                fournisseur = achat_form.cleaned_data['fournisseur']
                quantite = achat_form.cleaned_data['quantite']
                prix_unitaire = stock.prixUnitaire
                prix_totale = quantite * prix_unitaire


                achat_detail = achat_form.save(commit=False)
                achat_detail.prixTotale = prix_totale
                achat_detail.save()

                stock.quantite += quantite
                fournisseur.SoldeF+=prix_totale
                fournisseur.save()
                stock.save()

    else:
        achat_form = AchatDetailsForm(prefix='achat')

    return render(request, 'processus_achat.html', {'achat_form': achat_form, 'prix_totale': prix_totale})

def vente(request):
    prix_vente = 0
    quantitebool=1
    if request.method == 'POST':
        vente_form = VenteDetailsForm(request.POST, prefix='vente')
        if 'calculer_vente' in request.POST:
            if vente_form.is_valid():
                stock = vente_form.cleaned_data['stock']
                quantite = vente_form.cleaned_data['quantite']
                prix_vente = stock.prixVente
                prix_totale = quantite * prix_vente

        elif 'vendre' in request.POST:
            if vente_form.is_valid():
                stock = vente_form.cleaned_data['stock']
                client = vente_form.cleaned_data['client']
                quantite = vente_form.cleaned_data['quantite']
                prix_vente=stock.prixVente
                prix_totale = quantite * prix_vente

                vente_detail = vente_form.save(commit=False)
                vente_detail.prixTotale = prix_totale
                vente_detail.save()

                client.SoldeC+=prix_vente
                stock.quantite -= quantite
                if stock.quantite>=0 : 
                    stock.save()
                    client.save()
                else : 
                    quantitebool=0
                    

    else:
        vente_form = VenteDetailsForm(prefix='vente')

    return render(request, 'processus_vente.html', {'vente_form': vente_form, 'prix_vente': prix_vente , 'quantitebool':quantitebool})


def payementachat(request):
    solde = 0
    prixbool=0
    if request.method == 'POST':
        form = PayementAchatForm(request.POST)
        if form.is_valid():
            fournisseur = form.cleaned_data['fournisseur']
            if fournisseur.SoldeF>=form.cleaned_data['montantPaye']:
                fournisseur.SoldeF -= form.cleaned_data['montantPaye']
                solde = fournisseur.SoldeF
                fournisseur.save()
                form.save()
            else : 
                prixbool=1   
    else:
        form = PayementAchatForm()
    return render(request, 'payement_achat.html', {'payementachat': form , 'solde' : solde ,'prixbool':prixbool})

def payementvente(request):
    solde=0
    prixbool=0
    if request.method == 'POST':
        form = PayementVenteForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            if client.SoldeC>=form.cleaned_data['montantPaye']:
                client.SoldeC -= form.cleaned_data['montantPaye']
                solde=client.SoldeC
                client.save()
                form.save()  
            else : 
                prixbool=1 
    else:
        form = PayementVenteForm()
    return render(request, 'payement_vente.html', {'payementvente': form , 'solde':solde , 'prixbool':prixbool})

def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseur/fournisseur_list.html', {'fournisseurs': fournisseurs})

def fournisseur_detail(request, codeF):
    fournisseur = get_object_or_404(Fournisseur, codeF=codeF)
    return render(request, 'fournisseur/fournisseur_detail.html', {'fournisseur': fournisseur})

def fournisseur_create(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')
    else:
        form = FournisseurForm()
    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})

def fournisseur_edit(request, codeF):
    fournisseur = get_object_or_404(Fournisseur, codeF=codeF)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('fournisseur_list')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseur/fournisseur_form.html', {'form': form})

def fournisseur_delete(request, codeF):
    fournisseur = get_object_or_404(Fournisseur, codeF=codeF)
    fournisseur.delete()
    return redirect('fournisseur_list')

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client/client_list.html', {'clients': clients})

def client_detail(request, codeC):
    client = get_object_or_404(Client, codeC=codeC)
    return render(request, 'client/client_detail.html', {'client': client})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'client/client_form.html', {'form': form})

def client_edit(request, codeC):
    client = get_object_or_404(Client, codeC=codeC)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client/client_form.html', {'form': form})

def client_delete(request, codeC):
    client = get_object_or_404(Client, codeC=codeC)
    client.delete()
    return redirect('client_list')


def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock/stock_list.html', {'stocks': stocks})

def stock_detail(request, CodeP):
    stock = get_object_or_404(Stock, CodeP=CodeP)
    return render(request, 'stock/stock_detail.html', {'stock': stock})

def stock_create(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm()
    return render(request, 'stock/stock_form.html', {'form': form})

def stock_edit(request, CodeP):
    stock = get_object_or_404(Stock, CodeP=CodeP)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stock/stock_form.html', {'form': form})

def stock_delete(request, CodeP):
    stock = get_object_or_404(Stock, CodeP=CodeP)
    stock.delete()
    return redirect('stock_list')


def achat_details_list(request):
    achats = AchatDetails.objects.all()
    return render(request, 'achat/achat_details_list.html', {'achats': achats})

def achat_details_detail(request, id):
    achat = get_object_or_404(AchatDetails, id=id)
    return render(request, 'achat/achat_details_detail.html', {'achat': achat})

def achat_details_create(request):
    if request.method == 'POST':
        form = AchatDetailsForm(request.POST)
        if form.is_valid():
            formR=form.save(commit=False)
            stock=form.cleaned_data['stock']
            quantite=form.cleaned_data['quantite']
            fournisseur=form.cleaned_data['fournisseur']
            prix_totale=stock.prixUnitaire*quantite
            formR.prixTotale=prix_totale
            fournisseur.SoldeF+=prix_totale
            stock.quantite+=quantite
            stock.save()
            fournisseur.save()
            formR.save()
            return redirect('achat_details_list')

    else:
        form = AchatDetailsForm()
    return render(request, 'achat/achat_details_form.html', {'form': form ,})

def achat_details_edit(request, id):
    achat = get_object_or_404(AchatDetails, id=id)
    q=achat.quantite
    quantitebool=1
    if request.method == 'POST':
        form = AchatDetailsForm(request.POST, instance=achat)
        if form.is_valid():
            quantite_diff = form.cleaned_data['quantite'] - q
            stock = form.cleaned_data['stock']
            stock.quantite += quantite_diff
            fournisseur = form.cleaned_data['fournisseur']
            formR=form.save(commit=False)
            quantite=form.cleaned_data['quantite']
            prix_totale=stock.prixUnitaire*quantite
            formR.prixTotale=prix_totale
            fournisseur.SoldeF+=quantite_diff*stock.prixUnitaire
            if stock.quantite>=0: 
                fournisseur.save()
                stock.save()
                formR.save()
                return redirect('achat_details_list')
            else:
                quantitebool=0
    else:
        form = AchatDetailsForm(instance=achat)
    return render(request, 'achat/achat_details_form.html', {'form': form , 'quantitebool':quantitebool})

def achat_details_delete(request, id):
    achat = get_object_or_404(AchatDetails, id=id)
    quantitebool=1
    quantite=achat.quantite
    stock = achat.stock
    fournisseur=achat.fournisseur
    prix_totale=quantite*stock.prixUnitaire
    stock.quantite-=quantite
    fournisseur.SoldeF-=prix_totale
    if stock.quantite>=0 : 
        stock.save()
        fournisseur.save()
        achat.delete()
        return redirect('achat_details_list')
    else:
        quantitebool=0
        return render(request, 'achat/achat_details_detail.html', {'achat': achat , 'quantitebool':quantitebool})



def vente_details_list(request):
    ventes = VenteDetails.objects.all()
    return render(request, 'vente/vente_details_list.html', {'ventes': ventes})

def vente_details_detail(request, id):
    vente = get_object_or_404(VenteDetails, id=id)
    return render(request, 'vente/vente_details_detail.html', {'vente': vente})

def vente_details_create(request):
    quantitebool=1
    if request.method == 'POST':
        form = VenteDetailsForm(request.POST)
        if form.is_valid():
            formR=form.save(commit=False)
            
            client = form.cleaned_data['client']
            stock = form.cleaned_data['stock']
            quantite = form.cleaned_data['quantite']

            prix_totale=quantite*stock.prixVente
            
            stock.quantite-=quantite
            client.SoldeC+=prix_totale
            formR.prixTotale

            if stock.quantite>=0:
                client.save()
                stock.save()
                formR.save()
                return redirect('vente_details_list')
            else:
                quantitebool=0
    else:
        form = VenteDetailsForm()
    return render(request, 'vente/vente_details_form.html', {'form': form , 'quantitebool':quantitebool})

def vente_details_edit(request, id):
    vente = get_object_or_404(VenteDetails, id=id)
    q = vente.quantite
    quantitebool=1
    if request.method == 'POST':
        form = VenteDetailsForm(request.POST, instance=vente)
        if form.is_valid():
            formR = form.save(commit=False)

            client = form.cleaned_data['client']
            stock = form.cleaned_data['stock']
            quantite = form.cleaned_data['quantite']

            quantite_diff = quantite - q
            prix_totale = quantite * stock.prixVente

            stock.quantite-=quantite_diff
            client.SoldeC+=quantite_diff*stock.prixVente
            formR.prixTotale=prix_totale

            if stock.quantite>=0 : 
                stock.save()
                client.save()
                formR.save()
                return redirect('vente_details_list')
            else : 
                quantitebool=0
    else:
        form = VenteDetailsForm(instance=vente)
    return render(request, 'vente/vente_details_form.html', {'form': form , 'quantitebool':quantitebool})

def vente_details_delete(request, id):
    vente = get_object_or_404(VenteDetails, id=id)

    client = vente.client
    stock = vente.stock
    quantite = vente.quantite

    stock.quantite+=quantite
    client.SoldeC-=vente.quantite*stock.prixVente

    stock.save()
    client.save()

    vente.delete()
    return redirect('vente_details_list')

def payement_achat_list(request):
    payements = PayementAchat.objects.all()
    return render(request, 'payement/payement_achat_list.html', {'payements': payements})

def payement_achat_detail(request, id):
    payement = get_object_or_404(PayementAchat, id=id)
    return render(request, 'payement/payement_achat_detail.html', {'payement': payement})

def payement_achat_create(request):
    if request.method == 'POST':
        form = PayementAchatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payement_achat_list')
    else:
        form = PayementAchatForm()
    return render(request, 'payement/payement_achat_form.html', {'form': form})

def payement_achat_edit(request, id):
    payement = get_object_or_404(PayementAchat, id=id)
    if request.method == 'POST':
        form = PayementAchatForm(request.POST, instance=payement)
        if form.is_valid():
            form.save()
            return redirect('payement_achat_list')
    else:
        form = PayementAchatForm(instance=payement)
    return render(request, 'payement/payement_achat_form.html', {'form': form})

def payement_achat_delete(request, id):
    payement = get_object_or_404(PayementAchat, id=id)
    payement.delete()
    return redirect('payement_achat_list')


def payement_vente_list(request):
    payements = PayementVente.objects.all()
    return render(request, 'payement/payement_vente_list.html', {'payements': payements})

def payement_vente_detail(request, id):
    payement = get_object_or_404(PayementVente, id=id)
    return render(request, 'payement/payement_vente_detail.html', {'payement': payement})

def payement_vente_create(request):
    if request.method == 'POST':
        form = PayementVenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payement_vente_list')
    else:
        form = PayementVenteForm()
    return render(request, 'payement/payement_vente_form.html', {'form': form})

def payement_vente_edit(request, id):
    payement = get_object_or_404(PayementVente, id=id)
    if request.method == 'POST':
        form = PayementVenteForm(request.POST, instance=payement)
        if form.is_valid():
            form.save()
            return redirect('payement_vente_list')
    else:
        form = PayementVenteForm(instance=payement)
    return render(request, 'payement/payement_vente_form.html', {'form': form})

def payement_vente_delete(request, id):
    payement = get_object_or_404(PayementVente, id=id)
    payement.delete()
    return redirect('payement_vente_list')

def evolution_achats_annee(request, annee):
    achats_par_mois = AchatDetails.objects.filter(dateAchat__year=annee)\
                                         .values('dateAchat__month')\
                                         .annotate(total_achats=Sum('quantite'))

    mois_labels = [str(i) for i in range(1, 13)]
    achats_par_mois_dict = {achat['dateAchat__month']: achat['total_achats'] for achat in achats_par_mois}

    achats_evolution = [achats_par_mois_dict.get(mois, 0) for mois in range(1, 13)]

    context = {
        'annee': annee,
        'mois_labels_json': json.dumps(mois_labels),
        'achats_evolution_json': json.dumps(achats_evolution),
    }

    return render(request, 'evolution_achats_annee.html', context)

def evolution_ventes_annee(request, annee):
    ventes_par_mois = VenteDetails.objects.filter(dateVente__year=annee)\
                                         .values('dateVente__month')\
                                         .annotate(total_ventes=Sum('quantite'))

    mois_labels = [str(i) for i in range(1, 13)]
    ventes_par_mois_dict = {vente['dateVente__month']: vente['total_ventes'] for vente in ventes_par_mois}

    ventes_evolution = [ventes_par_mois_dict.get(mois, 0) for mois in range(1, 13)]

    context = {
        'annee': annee,
        'mois_labels_json': json.dumps(mois_labels),
        'ventes_evolution_json': json.dumps(ventes_evolution),
    }

    return render(request, 'evolution_ventes_annee.html', context)


def top_fournisseurs(request):
    top_fournisseurs = AchatDetails.objects.values('fournisseur__NomF')\
                                           .annotate(total_achats=Sum('prixTotale'))\
                                           .order_by('-total_achats')[:5]

    top_fournisseurs_json = json.dumps(list(top_fournisseurs), cls=DecimalEncoder)
    context = {
        'top_fournisseurs_json': top_fournisseurs_json,
    }

    return render(request, 'top_fournisseurs.html', context)

def top_clients(request):
    top_clients = VenteDetails.objects.values('client__NomC')\
                                           .annotate(total_ventes=Sum('prixTotale'))\
                                           .order_by('-total_ventes')[:5]

    top_clients_json = json.dumps(list(top_clients), cls=DecimalEncoder)
    context = {
        'top_clients_json': top_clients_json,
    }

    return render(request, 'top_clients.html', context)

def evolution_benefices_annee(request, annee):
    achats_par_mois = AchatDetails.objects.filter(dateAchat__year=annee)\
                                         .values('dateAchat__month')\
                                         .annotate(total_achats=Sum('quantite'))

    ventes_par_mois = VenteDetails.objects.filter(dateVente__year=annee)\
                                         .values('dateVente__month')\
                                         .annotate(total_ventes=Sum('quantite'))

    mois_labels = [str(i) for i in range(1, 13)]
    
    achats_par_mois_dict = {achat['dateAchat__month']: achat['total_achats'] for achat in achats_par_mois}
    ventes_par_mois_dict = {vente['dateVente__month']: vente['total_ventes'] for vente in ventes_par_mois}

    benefices_evolution = [(ventes_par_mois_dict.get(mois, 0) - achats_par_mois_dict.get(mois, 0)) for mois in range(1, 13)]

    context = {
        'annee': annee,
        'mois_labels_json': json.dumps(mois_labels),
        'benefices_evolution_json': json.dumps(benefices_evolution),
    }

    return render(request, 'evolution_benefices_annee.html', context)


def top_selling_products(request):
    top_products = VenteDetails.objects.values('stock__NomP')\
                                      .annotate(total_quantities=Sum('quantite'))\
                                      .order_by('-total_quantities')[:5]

    top_products_json = json.dumps(list(top_products), cls=DecimalEncoder)
    context = {
        'top_products_json': top_products_json,
    }

    return render(request, 'top_selling_products.html', context)

def faireTransfert(request):
    if request.method == 'POST':
        transfert=TransferDetailsForm(request.POST)
        if transfert.is_valid():
            stock = transfert.cleaned_data['Stock']
            stockcentre = StockCentre.objects.get(numC=transfert.cleaned_data['numC'], nomP=stock.NomP)
            stock.quantite-=transfert.cleaned_data['quantite']
            stockcentre.quantite+=transfert.cleaned_data['quantite']
            stockcentre.prixVente=stock.prixVente
            
            transfertmodel=transfert.save(commit=False)
            transfertmodel.cout=transfert.cleaned_data['quantite']*stock.prixUnitaire
            transfert.save()
            stock.save()
            stockcentre.save()
    else:
        transfert=TransferDetailsForm()
    return render(request,'Transfert.html',{'transfert':transfert})

def afficheEmployee(request,id):
    employee = get_object_or_404(Employee,id=id)
    return render(request,'Employe/EmployeAffiche.html',{'employee':employee})

def editEmployee(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST,instance=employee)
        if form.is_valid():
            form.save()
            return redirect('listeEmployee')
           
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'Employe/EmployeEdit.html', {'form': form })

def EmployeCreate(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeEmployee')
    else:
        form = EmployeeForm()
    return render(request, 'Employe/EmployeEdit.html', {'form': form})

def EmployeDelete(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('listeEmployee')

def demandeMasrouf(request):
    sommebool=0
    if request.method=='POST':
        form=MasroufForm(request.POST)
        if form.is_valid():
            somme=form.cleaned_data['somme']
            employee = form.cleaned_data['employee']
            if somme< (employee.salaire_mois):
                form.save()
                return redirect('listeEmployee')
            else : 
                sommebool=1
    else:
        form=MasroufForm()
    return render(request,'Employe/demandeMasrouf.html',{'form':form , 'sommebool':sommebool})

def Abcense(request):
    if request.method=='POST':
        form=AbcenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeEmployee')

    else:
        form=AbcenseForm()
    return render(request,'Employe/Abcense.html',{'form':form})

def listeEmployee(request):
    employes = Employee.objects.all()

    for employe in employes:
        employe.salaire_mois = employe.salaire_mois()

    return render(request, 'Employe/EmployesListe.html', {'employes': employes})

def vente2(request):
    prix_vente = 0
    quantitebool=1
    if request.method == 'POST':
        vente_form = VenteDetailsForm2(request.POST, prefix='vente')
        if 'calculer_vente' in request.POST:
            if vente_form.is_valid():
                stock = vente_form.cleaned_data['stockCentre']
                quantite = vente_form.cleaned_data['quantite']
                prix_vente = stock.prixVente
                prix_totale = quantite * prix_vente

        elif 'vendre' in request.POST:
            if vente_form.is_valid():
                stock = vente_form.cleaned_data['stockCentre']
                client = vente_form.cleaned_data['client']
                quantite = vente_form.cleaned_data['quantite']
                prix_vente=stock.prixVente
                prix_totale = quantite * prix_vente

                vente_detail = vente_form.save(commit=False)
                vente_detail.prixTotale = prix_totale
                vente_detail.save()

                client.SoldeC+=prix_vente
                stock.quantite -= quantite
                if stock.quantite>=0 : 
                    stock.save()
                    client.save()
                else : 
                    quantitebool=0
                    

    else:
        vente_form = VenteDetailsForm2(prefix='vente')

    return render(request, 'processus_vente2.html', {'vente_form': vente_form, 'prix_vente': prix_vente , 'quantitebool':quantitebool})