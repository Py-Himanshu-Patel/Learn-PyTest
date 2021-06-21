from django.contrib import admin
from .models import Transaction, Currency

class CurrencyAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

class TransactionAdmin(admin.ModelAdmin):
	list_display = ['name', 'email', 'currency', 'payment_intent_id', 'message']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Currency, CurrencyAdmin)
