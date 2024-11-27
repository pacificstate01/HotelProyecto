from django.urls import path,include
from .views import (
    ClientsView,
    ManageRoomsView,
    ManageClientsView,
    BookingView,
    ClientCreate,
    ClientDelete,
    ClientUpdate,
    ManageRoomCreate,
    ManageRoomDelete,
    ManageRoomUpdate,
    BookingViewCreate,
    BookingViewDelete,
    BookingViewUpdate,
    CambiarEstadoHab,
    CambiarEstadoRev)

urlpatterns = [
    path('clientes/',ClientsView.as_view(),name='clientes'),
    #URLS HABITACIONES
    path('gestion_hab/',ManageRoomsView.as_view(),name='gestion_hab'),
    path('gestion_hab/create/',ManageRoomCreate.as_view(),name='create_room'),
    path('gestion_hab/delete/<int:pk>',ManageRoomDelete.as_view(),name='delete_room'),
    path('gestion_hab/update/<int:pk>',ManageRoomUpdate.as_view(),name='update_room'),
    path('gestion_hab/nuevo_estado/<int:numero_habitacion>',CambiarEstadoHab.as_view(),name='limpieza'),

    #URLS CLIENTES
    path('gestion_cli/',ManageClientsView.as_view(),name='gestion_cli'),
    path('gestion_cli/create_cli/',ClientCreate.as_view(),name='client_create'),
    path('gestion_cli/delete/<str:numero_documento>/', ClientDelete.as_view(), name='client_delete'),
    path('gestion_cli/update/<str:numero_documento>/', ClientUpdate.as_view(), name='client_update'),
    #URLS RESERVAS
    path('reserva/',BookingView.as_view(),name='reserva'),
    path('reserva/create',BookingViewCreate.as_view(),name='create_reserva'),
    path('reserva/delete/<int:pk>',BookingViewDelete.as_view(),name='delete_reserva'),
    path('reserva/update/<int:pk>',BookingViewUpdate.as_view(),name='update_reserva'),
    path('reserva/updaterev/<str:codigo_reserva>',CambiarEstadoRev.as_view(),name='estado_limpieza'),

    ]
