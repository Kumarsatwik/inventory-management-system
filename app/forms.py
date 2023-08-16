from django import forms
from .models import Inventory, Orders, Transaction


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name',  'image', 'cost', 'quantity', 'selling_price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['item', 'quantity', 'cost', 'is_received', 'is_cancel']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity',]
