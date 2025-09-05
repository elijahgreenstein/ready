import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView

from .forms import CreateFoodForm, CreateFirstAidForm, CreateSuppliesForm
from .models import Category, Group, Item, ItemInstance, Location, Unit

def index(request):
    """View function for home page"""
    today = datetime.date.today()
    exp_warning = today + datetime.timedelta(days=90)

    food_items = Item.objects \
                     .filter(category__name='Food')
    firstaid_items = Item.objects \
                          .filter(category__name='First Aid')
    supplies_items = Item.objects \
                         .filter(category__name='Supplies')

    food_instances = ItemInstance.objects \
                                 .filter(item__category__name='Food') \
                                 .filter(status='a')
    firstaid_instances = ItemInstance.objects \
                                     .filter(item__category__name='First Aid') \
                                     .filter(status='a')
    supplies_instances = ItemInstance.objects \
                                     .filter(item__category__name='Supplies') \
                                     .filter(status='a')

    num_food = food_instances.count()
    num_firstaid = firstaid_instances.count()
    num_supplies = supplies_instances.count()

    food_warnings = food_instances.filter(expiration_date__gt=today).filter(expiration_date__lt=exp_warning)
    food_emergencies = food_instances.filter(expiration_date__lt=today)

    firstaid_warnings = firstaid_instances.filter(expiration_date__gt=today).filter(expiration_date__lt=exp_warning)
    firstaid_emergencies = firstaid_instances.filter(expiration_date__lt=today)

    supplies_warnings = supplies_instances.filter(expiration_date__gt=today).filter(expiration_date__lt=exp_warning)
    supplies_emergencies = supplies_instances.filter(expiration_date__lt=today)

    food_quant_warnings = []
    food_quant_emergencies = []
    for food in food_items.filter(target_quantity__isnull=False):
        if food.total_quantity() <= food.target_quantity / 2:
            food_quant_emergencies.append(food)
        elif food.total_quantity() < food.target_quantity:
            food_quant_warnings.append(food)

    firstaid_quant_warnings = []
    firstaid_quant_emergencies = []
    for firstaid in firstaid_items.filter(target_quantity__isnull=False):
        if firstaid.total_quantity() <= firstaid.target_quantity / 2:
            firstaid_quant_emergencies.append(firstaid)
        elif firstaid.total_quantity() < firstaid.target_quantity:
            firstaid_quant_warnings.append(firstaid)

    supplies_quant_warnings = []
    supplies_quant_emergencies = []
    for supplies in supplies_items.filter(target_quantity__isnull=False):
        if supplies.total_quantity() <= supplies.target_quantity / 2:
            supplies_quant_emergencies.append(supplies)
        elif supplies.total_quantity() < supplies.target_quantity:
            supplies_quant_warnings.append(supplies)

    food_groups = Group.objects.filter(category__name='Food')
    firstaid_groups = Group.objects.filter(category__name='First Aid')
    supplies_groups = Group.objects.filter(category__name='Supplies')

    locations = Location.objects.all()

    context = {
        'food_items': food_items,
        'firstaid_items': firstaid_items,
        'supplies_items': supplies_items,
        'num_food': num_food,
        'num_firstaid': num_firstaid,
        'num_supplies': num_supplies,
        'food_warnings': food_warnings,
        'food_emergencies': food_emergencies,
        'firstaid_warnings': firstaid_warnings,
        'firstaid_emergencies': firstaid_emergencies,
        'supplies_warnings': supplies_warnings,
        'supplies_emergencies': supplies_emergencies,
        'food_quant_warnings': food_quant_warnings,
        'food_quant_emergencies': food_quant_emergencies,
        'firstaid_quant_warnings': firstaid_quant_warnings,
        'firstaid_quant_emergencies': firstaid_quant_emergencies,
        'supplies_quant_warnings': supplies_quant_warnings,
        'supplies_quant_emergencies': supplies_quant_emergencies,
        'food_groups': food_groups,
        'firstaid_groups': firstaid_groups,
        'supplies_groups': supplies_groups,
        'locations': locations,
    }

    return render(request, 'ready/index.html', context)

class LocationDetailView(generic.DetailView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['locations'] = Location.objects.all()
        return context

class ItemDetailView(generic.DetailView):
    model = Item

class ItemInstanceDetailView(generic.DetailView):
    model = ItemInstance

class FoodCreateView(CreateView):
    model = ItemInstance
    form_class = CreateFoodForm
    template_name = 'ready/food_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='Food')
        return context

class FirstAidCreateView(CreateView):
    model = ItemInstance
    form_class = CreateFirstAidForm
    template_name = 'ready/firstaid_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='First Aid')
        return context

class SuppliesCreateView(CreateView):
    model = ItemInstance
    form_class = CreateSuppliesForm
    template_name = 'ready/supplies_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='Supplies')
        return context

class FoodUpdate(UpdateView):
    model = ItemInstance
    form_class = CreateFoodForm
    template_name = 'ready/food_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='Food')
        return context

class FirstAidUpdate(UpdateView):
    model = ItemInstance
    form_class = CreateFoodForm
    template_name = 'ready/firstaid_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='First Aid')
        return context

class SuppliesUpdate(UpdateView):
    model = ItemInstance
    form_class = CreateFoodForm
    template_name = 'ready/supplies_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['item'].queryset = Item.objects.filter(category__name='Supplies')
        return context

def consume_item(request, pk):
    instance = ItemInstance.objects.get(id=pk)
    instance.status = 'c'
    instance.save()
    return HttpResponseRedirect('/ready')

def store_item(request, pk):
    instance = ItemInstance.objects.get(id=pk)
    instance.status = 's'
    instance.save()
    return HttpResponseRedirect('/ready')
