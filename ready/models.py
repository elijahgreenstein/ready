from django.db import models
from django.urls import reverse

import datetime, uuid

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the category name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the group name')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=20, help_text='Enter the unit abbreviation or name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the store name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100, help_text='Enter the location name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('location-detail', args=[str(self.id)])

class Note(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, help_text='Enter a short title for the note')
    content = models.TextField(max_length=2000, help_text='Enter the note here')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 50, help_text='Enter the item name')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    target_quantity = models.FloatField(blank=True, null=True, help_text='Enter the amount that should be in supply')
    amount_for_pricing = models.FloatField(blank=True, null=True, help_text='Enter the base amount for calculating the average price')

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-detail', args=[str(self.id)])

    def total_quantity(self):
        return sum([item.quantity for item in self.iteminstance_set.filter(status='a')])

    def quantity_status(self):
        if self.total_quantity() <= self.target_quantity / 2:
            quantity_status = 'emergency'
        elif self.total_quantity() < self.target_quantity:
            quantity_status = 'warning'
        else:
            quantity_status = 'safe'
        return quantity_status

    def count_available_items(self):
        return self.iteminstance_set.filter(status='a').count()

    def get_available_items(self):
        return self.iteminstance_set.filter(status='a')

    def average_price(self):
        prices = []
        if self.amount_for_pricing and self.iteminstance_set.all():
            for inst in self.iteminstance_set.all():
                if inst.price and inst.quantity:
                    prices.append(inst.price / inst.quantity)
            return "{:.2f}".format((sum(prices) / len(prices)) * self.amount_for_pricing)
        else:
            return(None)

class ItemInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular item')
    info = models.CharField(max_length = 100, help_text='Enter basic details of the item')
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text='Enter the quantity in units of this item type')
    price = models.FloatField(blank=True, null=True, help_text='Enter the price')
    purchase_date = models.DateField(blank=True, null=True, help_text='Enter the date purchased (if known)')
    expiration_date = models.DateField(blank=True, null=True, help_text='Enter the expiration date (if there is one)')
    timestamp = models.DateTimeField(auto_now=True)

    ITEM_STATUS = (
        ('a', 'Available'),
        ('s', 'Stored'),
        ('c', 'Consumed'),
    )

    status = models.CharField(
        max_length=1,
        choices=ITEM_STATUS,
        blank=True,
        null=True,
        default='a',
        help_text='Status of the item',
    )

    note = models.TextField(max_length=1000, blank=True, null=True, help_text='Enter an optional note')

    class Meta:
        ordering = ['status', 'item', 'expiration_date', 'info', ]

    def __str__(self):
        return self.info

    def get_absolute_url(self):
        return reverse('item-instance-detail', args=[str(self.id)])

    def get_unit(self):
        return self.item.unit

    get_unit.short_description = 'Unit'

    def exp_status(self):
        if self.expiration_date < datetime.date.today():
            exp_status = 'expired'
        elif self.expiration_date < datetime.date.today() + datetime.timedelta(days=90):
            exp_status = 'warning'
        else:
            exp_status = 'safe'
        return exp_status

    def price_per_unit(self):
        if self.item.amount_for_pricing and self.price:
            return "{:.2f}".format(self.price / self.quantity * self.item.amount_for_pricing)
