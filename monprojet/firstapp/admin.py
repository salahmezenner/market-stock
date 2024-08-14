from django.contrib import admin
from .models import Client,Fournisseur,Stock,AchatDetails,VenteDetails,PayementAchat,PayementVente,StockCentre,TransferDetails,Employee
from .models import Massrouf , Abcense

class ClientAdmin(admin.ModelAdmin):
    list_display = ('codeC', 'NomC', 'PrenomC' , 'TelC','AdressC' , 'SoldeC')

admin.site.register(Client, ClientAdmin)
admin.site.register(Fournisseur)
admin.site.register(Stock)
admin.site.register(AchatDetails)
admin.site.register(VenteDetails)
admin.site.register(PayementAchat)
admin.site.register(PayementVente)
admin.site.register(StockCentre)
admin.site.register(TransferDetails)
admin.site.register(Employee)
admin.site.register(Massrouf)
admin.site.register(Abcense)
