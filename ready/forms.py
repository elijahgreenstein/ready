from django import forms
from django.forms import ModelForm

from ready.models import ItemInstance

class CreateFoodForm(ModelForm):
    class Meta:
        model = ItemInstance
        fields = ['info', 'item', 'quantity', 'price', 'store', 'purchase_date', 'expiration_date', 'location', 'status', 'note']
        widgets = {
            'purchase_date': forms.DateInput,
            'expiration_date': forms.DateInput,
        }

class CreateFirstAidForm(ModelForm):
    class Meta:
        model = ItemInstance
        fields = ['info', 'item', 'quantity', 'price', 'store', 'purchase_date', 'expiration_date', 'location', 'status', 'note']
        widgets = {
            'purchase_date': forms.DateInput,
            'expiration_date': forms.DateInput,
        }

class CreateSuppliesForm(ModelForm):
    class Meta:
        model = ItemInstance
        fields = ['info', 'item', 'quantity', 'price', 'store', 'purchase_date', 'expiration_date', 'location', 'status', 'note']
        widgets = {
            'purchase_date': forms.DateInput,
            'expiration_date': forms.DateInput,
        }
