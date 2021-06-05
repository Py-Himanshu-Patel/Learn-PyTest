from django.contrib import admin
from .models import Transaction, Currency

admin.site.register(Transaction)
admin.site.register(Currency)
