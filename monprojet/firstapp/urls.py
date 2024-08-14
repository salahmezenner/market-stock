from django.urls import path
from django.views.generic.base import TemplateView
from .views import achat, vente, payementachat, payementvente, vente2
from .views import fournisseur_list, fournisseur_detail, fournisseur_create, fournisseur_edit, fournisseur_delete
from .views import client_list, client_edit, client_create, client_delete, client_detail , faireTransfert
from .views import stock_list, stock_detail, stock_create, stock_edit, stock_delete
from .views import achat_details_list, achat_details_detail, achat_details_create, achat_details_edit, achat_details_delete
from .views import vente_details_list, vente_details_detail, vente_details_create, vente_details_edit, vente_details_delete
from .views import payement_achat_list, payement_achat_detail, payement_achat_create, payement_achat_edit, payement_achat_delete
from .views import payement_vente_list, payement_vente_detail, payement_vente_create, payement_vente_edit, payement_vente_delete
from .views import evolution_achats_annee , evolution_ventes_annee ,top_fournisseurs , top_clients  , evolution_benefices_annee , top_selling_products
from .views import listeEmployee , editEmployee , afficheEmployee , EmployeDelete , EmployeCreate, demandeMasrouf , Abcense

urlpatterns = [    
    path('achat/', achat, name='achat'),
    path('vente/', vente, name='vente'),
    path('payementachat/', payementachat, name='payementachat'),
    path('payementvente/', payementvente, name='payementvente'), 
    path('fournisseurs/', fournisseur_list, name='fournisseur_list'),
    path('fournisseurs/<int:codeF>/', fournisseur_detail, name='fournisseur_detail'),
    path('fournisseurs/new/', fournisseur_create, name='fournisseur_create'),
    path('fournisseurs/<int:codeF>/edit/', fournisseur_edit, name='fournisseur_edit'),
    path('fournisseurs/<int:codeF>/delete/', fournisseur_delete, name='fournisseur_delete'),
    path('clients/', client_list, name='client_list'),
    path('clients/<int:codeC>/', client_detail, name='client_detail'),
    path('clients/new/', client_create, name='client_create'),
    path('clients/<int:codeC>/edit/', client_edit, name='client_edit'),
    path('clients/<int:codeC>/delete/', client_delete, name='client_delete'),
    path('stocks/', stock_list, name='stock_list'),
    path('stocks/<int:CodeP>/', stock_detail, name='stock_detail'),
    path('stocks/new/', stock_create, name='stock_create'),
    path('stocks/<int:CodeP>/edit/', stock_edit, name='stock_edit'),
    path('stocks/<int:CodeP>/delete/', stock_delete, name='stock_delete'),
    path('achatdetails/', achat_details_list, name='achat_details_list'),
    path('achatdetails/<int:id>/', achat_details_detail, name='achat_details_detail'),
    path('achatdetails/new/', achat_details_create, name='achat_details_create'),
    path('achatdetails/<int:id>/edit/', achat_details_edit, name='achat_details_edit'),
    path('achatdetails/<int:id>/delete/', achat_details_delete, name='achat_details_delete'),
    path('ventedetails/', vente_details_list, name='vente_details_list'),
    path('ventedetails/<int:id>/', vente_details_detail, name='vente_details_detail'),
    path('ventedetails/new/', vente_details_create, name='vente_details_create'),
    path('ventedetails/<int:id>/edit/', vente_details_edit, name='vente_details_edit'),
    path('ventedetails/<int:id>/delete/', vente_details_delete, name='vente_details_delete'),    
    path('payementachats/', payement_achat_list, name='payement_achat_list'),
    path('payementachats/<int:id>/', payement_achat_detail, name='payement_achat_detail'),
    path('payementachats/new/', payement_achat_create, name='payement_achat_create'),
    path('payementachats/<int:id>/edit/', payement_achat_edit, name='payement_achat_edit'),
    path('payementachats/<int:id>/delete/', payement_achat_delete, name='payement_achat_delete'),
    path('payementventes/', payement_vente_list, name='payement_vente_list'),
    path('payementventes/<int:id>/', payement_vente_detail, name='payement_vente_detail'),
    path('payementventes/new/', payement_vente_create, name='payement_vente_create'),
    path('payementventes/<int:id>/edit/', payement_vente_edit, name='payement_vente_edit'),
    path('payementventes/<int:id>/delete/', payement_vente_delete, name='payement_vente_delete'),
    path('evolution-achats-annee/<int:annee>/', evolution_achats_annee, name='evolution_achats_annee'),
    path('evolution-ventes-annee/<int:annee>/', evolution_ventes_annee, name='evolution_ventes_annee'),
    path('top-fournisseurs/', top_fournisseurs, name='top_fournisseurs'),
    path('top-clients/', top_clients, name='top_clients'),
    path('evolution-benefices/<int:annee>/', evolution_benefices_annee, name='evolution_benefices_annee'),
    path('top-selling-products/', top_selling_products, name='top_selling_products'),
    path('principale/', TemplateView.as_view(template_name='principale.html'), name='principale'),
    path('faireTransfert/', faireTransfert, name='faireTransfert'),
    path('Employe/EmployeListe/',listeEmployee,name='listeEmployee'),
    path('Employe/<int:id>/edit/',editEmployee ,name='EmployeEdit'),
    path('Employe/<int:id>/delete/', EmployeDelete, name='EmployeDelete'),
    path('Employe/<int:id>/', afficheEmployee, name='afficheEmployee'),
    path('Employe/new',EmployeCreate,name='EmployeCreate'),
    path('Employe/demandeMasrouf',demandeMasrouf,name='demandeMasrouf'),
    path('Employe/Abcense',Abcense,name='Abcense'),
    path('vente2/', vente2, name='vente2'),

    ]
