from django.urls import path

from .views import *


table_list = CreateListTableViewSet.as_view(
    {'get': 'list',
    'post': 'create'}
    )

reserv_list = CreateListReservationViewSet.as_view(
    {'get': 'list',
    'post': 'create'}
    )

urlpatterns = [
    path('tables/', table_list, name='table_list'),
    path('tables/<int:pk>/', DeleteTableAPIView.as_view(), name='table_delete'),
    path('reservations/', reserv_list, name='reserv_list'),
    path('reservations/<int:pk>/', DeleteReservationAPIView.as_view(), name='reserv_delete'),
]
