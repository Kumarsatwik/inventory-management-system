from django.shortcuts import render, redirect, get_object_or_404
from .forms import InventoryForm, OrderForm, TransactionForm
from .models import Inventory, Orders, Transaction
from django.db.models import Q
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from datetime import datetime
# Create your views here.


def home(request):
    items = Inventory.objects.filter()
    total_profit = sum(i.profit_earned for i in items)
    total_revenue = sum(i.revenue for i in items)
    total_cost = sum(i.cost for i in items)
    items_in_stock = items.filter(quantity__gt=0).count()
    highest_cost_item = items.order_by('-cost').first()

    order = Orders.objects.all()
    transaction = Transaction.objects.all()

    now = datetime.now()
    current_month = now.month

    context = {
        'total_profit': total_profit,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'items_in_stock': items_in_stock,
        'highest_cost_item': highest_cost_item,
        'willbeRecieved': order.filter(Q(is_cancel=False) & Q(is_received=False)).count(),
        'no_of_order': order.count(),
        'total_order_cost': sum(i.cost for i in order),
        'cancel_order': order.filter(is_cancel=True).count(),
        'min_quantity': items.order_by('quantity').first().quantity,
        'highest_profit_item': items.order_by('-profit_earned').first().profit_earned,
        'total_transaction': transaction.count(),
        'most_active_month': transaction.annotate(month=ExtractMonth('transactiondttm')).values(
            'month').annotate(count=Count('id')).order_by('-count').first(),
        'current_month': transaction.filter(transactiondttm__month=current_month).annotate(month=ExtractMonth('transactiondttm')).aggregate(
    count=Count('id')
)['count']
    }
    return render(request, 'home.html', context)


def item_list(request):
    items = Inventory.objects.all()
    context = {'items': items}
    return render(request, 'item_list.html', context)


def add_item(request):
    # View to create new item
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES)
        # print(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            cost = form.cleaned_data['cost']
            selling_price = form.cleaned_data['selling_price']
            if cost > selling_price:
                return render(request, 'createItem.html', {'message': "Selling Price  must be greater than Cost", 'form': form})
            form.save()
            return redirect('item_list')
        else:
            print(form.errors)
    else:
        form = InventoryForm()

    context = {'form': form}
    return render(request, 'createItem.html', context)


def item_details(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    orders = Orders.objects.filter(item=item)
    transactions = Transaction.objects.filter(item=item)
    context = {
        'item': item,
        'orders': orders,
        'transactions': transactions
    }
    # print(context)
    return render(request, 'item_details.html', context)


def edit_item(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('item_details', pk=item.pk)
        else:
            print(form.errors)
    else:
        form = InventoryForm(instance=item)
    context = {'form': form}
    return render(request, 'edit_item.html', context)


def sell_item(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        sell_quantity = int(request.POST.get('quantity'))
        if sell_quantity == 0:
            return render(request, 'sell_item.html', {'item': item, 'message': 'Sell quantity cant be Zero'})
        if int(item.quantity) < sell_quantity:
            return render(request, 'sell_item.html', {'item': item, 'message': 'Insufficient quantity'})
        item.quantity_sold += sell_quantity
        item.revenue += sell_quantity*item.cost
        item.quantity -= sell_quantity
        item.profit_earned += sell_quantity * \
            (int(item.selling_price)-int(item.cost))
        item.save()

        Transaction.objects.create(
            name=item.name, item=item, quantity=sell_quantity, selling_price=sell_quantity*item.selling_price)
        return redirect('item_details', pk=item.pk)
    else:
        context = {
            'item': item
        }
        return render(request, 'sell_item.html', context)


def order_list(request):
    query = request.GET.get('q')
    if query:
        # If a search query is provided, filter the orders by name or any other relevant fields.
        orders = Orders.objects.filter(
            # Search by name (modify the field as needed)
            Q(name__icontains=query) |
            # Search by cost (modify the field as needed)
            Q(cost__icontains=query) |
            # Search by order date (modify the field as needed)
            Q(orderdttm__icontains=query)
        )
    else:
        # If no search query is provided, return all orders.
        orders = Orders.objects.all()

    context = {
        'orders': orders,
        'search_query': query or ""
    }
    return render(request, 'order_list.html', context)


def order_item(request, pk):
    item = get_object_or_404(Inventory, id=pk)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Save the form without committing to the database
            order = form.save(commit=False)
            order.name = item.name
            order.item = item  # Associate the item with the order
            order.save()  # Save the order to the database
            # You can access cleaned data after saving
            print("Form saved:", form.cleaned_data)
            return redirect('item_details', pk=item.pk)
        else:
            print("Form invalid:", form.errors)

    else:
        # Set initial values in the form
        form = OrderForm(initial={'item': item, 'cost': item.cost})

        form.fields['cost'].widget.attrs['readonly'] = True
        form.fields['item'].widget.attrs['readonly'] = True

    return render(request, 'order.html', {'form': form})


def edit_order(request, pk):
    order = get_object_or_404(Orders, id=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            if form.cleaned_data['is_received'] == True:
                item = get_object_or_404(Inventory, id=order.item.id)
                item.quantity += order.quantity
                item.save()

            form.save()
            return redirect('item_details', pk=order.item.id)
    else:
        form = OrderForm(instance=order)

    initial_item = order.item if order.item else None
    form.fields['item'].initial = initial_item

    return render(request, 'edit_order.html', {'form': form})


def transaction_list(request):
    query = request.GET.get('q')
    if query:
        # If a search query is provided, filter the orders by name or any other relevant fields.
        Transactions = Transaction.objects.filter(
            name__icontains=query
        )
    else:
        # If no search query is provided, return all orders.
        Transactions = Transaction.objects.all()

    context = {
        'transactions': Transactions,
        'search_query': query or ""
    }
    return render(request, 'transaction_list.html', context)
