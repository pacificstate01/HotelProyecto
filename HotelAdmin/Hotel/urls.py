from django.urls import path,include
from .views import ClientsView,ManageRoomsView,ManageClientsView,BookingView,ClientCreate,ClientDelete,ClientUpdate

urlpatterns = [
    path('clientes/',ClientsView.as_view(),name='clientes'),
    path('gestion_hab/',ManageRoomsView.as_view(),name='gestion_hab'),
    path('gestion_cli/',ManageClientsView.as_view(),name='gestion_cli'),
    path('gestion_cli/create_cli/',ClientCreate.as_view(),name='client_create'),
    path('gestion_cli/delete/<int:id>/', ClientDelete.as_view(), name='client_delete'),
    path('gestion_cli/update/<int:id>/', ClientUpdate.as_view(), name='client_update'),
    path('reserva/',BookingView.as_view(),name='reserva'),
]
