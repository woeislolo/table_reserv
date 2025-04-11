from rest_framework.serializers import ModelSerializer

from .models import *


class TableSerializer(ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'seats', 'location']


class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'customer_name', 'table_id', 'reservation_time', 'duration_minutes']
        