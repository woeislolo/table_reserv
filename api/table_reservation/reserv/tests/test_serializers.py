from datetime import datetime

from django.test import TestCase

from reserv.models import *
from reserv.serializers import *


class TableSerializerTestCase(TestCase):
    def setUp(self):

        self.table1 = Table.objects.create(name='Table 1',
                                           seats=4,
                                           location=1)

        self.table2 = Table.objects.create(name='Table 2',
                                           seats=3,
                                           location=2)
        
    def test_table_serializer_ok(self):
        tables = Table.objects.all()
        data = TableSerializer(tables, many=True).data
        expected_data = [
            {
                'id': self.table1.id, 
                'name': 'Table 1', 
                'seats': 4, 
                'location': '1'
                }, 
            {
                'id': self.table2.id, 
                'name': 'Table 2', 
                'seats': 3, 
                'location': '2'
                }
        ]

        self.assertEqual(data, expected_data)


class ReservationSerializerTestCase(TestCase):
    def setUp(self):

        self.table1 = Table.objects.create(name='Table 1',
                                           seats=4,
                                           location=1)

        self.table2 = Table.objects.create(name='Table 2',
                                           seats=3,
                                           location=2)
        
        self.reservation1 = Reservation.objects.create(customer_name='Петя Иванов',
                                           table_id=self.table1,
                                           reservation_time=datetime(2025, 10, 1, 10),
                                           duration_minutes=60)
        
        self.reservation2 = Reservation.objects.create(customer_name='Саша Иванов',
                                           table_id=self.table1,
                                           reservation_time=datetime(2025, 10, 1, 12, 30),
                                           duration_minutes=90)
        
    def test_reservation_serializer_ok(self):
        reservations = Reservation.objects.all()
        data = ReservationSerializer(reservations, many=True).data
        expected_data = [
            {
                'id': self.reservation1.id, 
                'customer_name': 'Петя Иванов', 
                'table_id': self.table1.id, 
                'reservation_time': '2025-10-01T10:00:00Z', # ? не уверена в формате
                'duration_minutes': 60
                }, 
            {
                'id': self.reservation2.id, 
                'customer_name': 'Саша Иванов', 
                'table_id': self.table1.id, 
                'reservation_time': '2025-10-01T12:30:00Z', 
                'duration_minutes': 90
                }
            ]

        self.assertEqual(data, expected_data)
