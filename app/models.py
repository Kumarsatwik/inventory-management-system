from django.db import models
import datetime
import uuid


class Inventory(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Name")
    image = models.ImageField(
        verbose_name="Item Image", upload_to='ItemImage/')
    iin = models.UUIDField(
        default=uuid.uuid4, editable=False, verbose_name="IIN")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Cost")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    quantity_sold = models.PositiveIntegerField(
        default=0, verbose_name="Quantity Sold")
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Selling Price")
    profit_earned = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Profit Earned")
    revenue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Revenue")

    class Meta:
        verbose_name_plural = "Inventory"

    def __str__(self):
        return self.name


class Orders(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Name")
    item = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, verbose_name="Item")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Cost")
    orderdttm = models.DateTimeField(
        auto_now_add=True, verbose_name="Order Date and Time")
    is_received = models.BooleanField(
        default=False, verbose_name="Is Received")
    is_cancel = models.BooleanField(default=False, verbose_name="Is Cancelled")

    class Meta:
        verbose_name_plural = "Orders"


class Transaction(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=100, verbose_name="Name")
    item = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, verbose_name="Item")
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Selling Price")
    transactiondttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name="Transaction Date and Time")

    class Meta:
        verbose_name_plural = "Transactions"
