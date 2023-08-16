from django.contrib import admin
from .models import *
# Register your models here.


class InventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'iin', 'cost', 'quantity',
                    'quantity_sold', 'selling_price', 'profit_earned', 'revenue']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'item', 'quantity',
                    'selling_price', 'transactiondttm']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'item', 'quantity',
                    'cost', 'orderdttm', 'is_received', 'is_cancel']


admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Orders, OrdersAdmin)
