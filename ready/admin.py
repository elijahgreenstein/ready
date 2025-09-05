from django.contrib import admin

from .models import Category, Group, Unit, Store, Location, Note, Item, ItemInstance

admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Unit)
admin.site.register(Store)
admin.site.register(Location)
admin.site.register(Note)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'group', 'unit']

@admin.register(ItemInstance)
class ItemInstanceAdmin(admin.ModelAdmin):
    list_display = ['item', 'info', 'purchase_date', 'expiration_date', 'quantity', 'get_unit','status']
