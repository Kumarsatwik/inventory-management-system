from django.utils import timezone
from datetime import timedelta
import random
from app.models import Inventory, Orders, Transaction
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inventory.settings")
django.setup()


def generate_iin():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))


def create_items(num):
    for i in range(num):
        Inventory.objects.create(
            name=f'Item {i}',
            iin=generate_iin(),
            cost=random.uniform(11, 30),
            quantity=random.randint(31, 70),
            selling_price=random.uniform(10, 200)
        )


def create_orders(num):
    items = Inventory.objects.all()
    for i in range(num):
        item = random.choice(items)
        Orders.objects.create(
            item=item,
            quantity=random.randint(1, 10)
        )


def create_transactions(num):
    items = Inventory.objects.all()
    for i in range(num):
        item = random.choice(items)
        Transaction.objects.create(
            item=item,
            quantity=random.randint(1, 5),
            selling_price=item.selling_price * random.randint(1, 5),
            transaction_dtm=timezone.now() - timedelta(days=random.randint(1, 30))
        )

# Run


create_items(10)
# create_orders(10)
# create_transactions(10)
