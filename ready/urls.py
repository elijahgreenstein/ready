from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Locations
    path('location/<int:pk>', views.LocationDetailView.as_view(), name='location-detail'),
    # Details
    path('item/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('instance/<uuid:pk>', views.ItemInstanceDetailView.as_view(), name='item-instance-detail'),
    # Create
    path('food/create', views.FoodCreateView.as_view(), name='food-create'),
    path('firstaid/create', views.FirstAidCreateView.as_view(), name='firstaid-create'),
    path('supplies/create', views.SuppliesCreateView.as_view(), name='supplies-create'),
    # Update
    path('food/<uuid:pk>/update/', views.FoodUpdate.as_view(), name='food-update'),
    path('firstaid/<uuid:pk>/update/', views.FirstAidUpdate.as_view(), name='firstaid-update'),
    path('supplies/<uuid:pk>/update/', views.SuppliesUpdate.as_view(), name='supplies-update'),
    # Change Item Instance Status
    path('consume/<uuid:pk>', views.consume_item, name='consume-item'),
    path('store/<uuid:pk>', views.store_item, name='store-item'),
]

