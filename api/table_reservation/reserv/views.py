from datetime import timedelta

import logging

from rest_framework import viewsets, mixins, generics
from rest_framework import status
from rest_framework.response import Response

from .models import *
from .serializers import *


logger = logging.getLogger('reserv')


def log_exception(status_code, data):
    if 400 <= status_code < 500:
        logger.error(f'({status_code}, {data})')
    elif 300 <= status_code < 400:
        logger.warning(f'({status_code}, {data})')


class CreateListTableViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """ Получить список всех столиков либо добавить новый """

    queryset = Table.objects.all()
    serializer_class = TableSerializer
    
    def handle_exception(self, exc):
        exc = super().handle_exception(exc)
        log_exception(exc.status_code, exc.data)
        return exc


class DeleteTableAPIView(generics.DestroyAPIView):
    """ Удалить столик """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def handle_exception(self, exc):
        exc = super().handle_exception(exc)
        log_exception(exc.status_code, exc.data)
        return exc


class CreateListReservationViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """ Получить список всех броней либо добавить новую """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        table_id = serializer.validated_data['table_id']
        reserv_time = serializer.validated_data['reservation_time']
        duration = serializer.validated_data['duration_minutes']

        new_slot_start_time = reserv_time.time()
        new_slot_end_time = (reserv_time + timedelta(minutes=duration)).time()

        slots = Reservation.objects. \
            filter(table_id=table_id). \
            filter(reservation_time__day=reserv_time.day)
        for slot in slots:
            slot_start_time = slot.reservation_time.time()
            slot_end_time = (slot.reservation_time + timedelta(minutes=slot.duration_minutes)).time()

            if not (new_slot_start_time >= slot_end_time or new_slot_end_time <= slot_start_time):
                logger.error('(400, {"message": "new reservations time was blocked by existing reservations"})')
                return Response({'message': 'Время добавляемой брони пересекается с уже существующими'}, 
                                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def handle_exception(self, exc):
        exc = super().handle_exception(exc)
        log_exception(exc.status_code, exc.data)
        return exc


class DeleteReservationAPIView(generics.DestroyAPIView):
    """ Удалить бронь """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def handle_exception(self, exc):
        exc = super().handle_exception(exc)
        log_exception(exc.status_code, exc.data)
        return exc
