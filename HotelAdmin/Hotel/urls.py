from django.urls import path,include
from .views import MenuView,ClientsView,ManageRoomsView,ManageClientsView,BookingView

urlpatterns = [
    path('menu/',MenuView.as_view(),name='menu'),
    path('clientes/',ClientsView.as_view(),name='clientes'),
    path('gestion_hab/',ManageRoomsView.as_view(),name='gestion_hab'),
    path('gestion_cli/',ManageClientsView.as_view(),name='gestion_cli'),
    path('reserva/',BookingView.as_view(),name='reserva'),

]
