from django.contrib import admin
from .models import Transaction, Currency

class CurrencyAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

admin.site.register(Transaction)
admin.site.register(Currency, CurrencyAdmin)
