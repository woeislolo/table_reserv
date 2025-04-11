import json
from datetime import datetime

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from reserv.models import *
from reserv.serializers import *


class TableAPITestCase(APITestCase):
    def setUp(self):

        self.table1 = Table.objects.create(name='Table 1',
                                           seats=4,
                                           location=1)

        self.table2 = Table.objects.create(name='Table 2',
                                           seats=3,
                                           location=2)

    def test_get_all_tables(self):
        url = reverse('table_list')
        response = self.client.get(url)
        tables = Table.objects.all()
        serializer_data = TableSerializer(tables, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)


    def test_create_a_table(self):
        url = reverse('table_list')
        data = {
            'name': 'Table 3',
            'seats': 4,
            'location': 1,
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.all().count(), 3)
        self.assertEqual(Table.objects.last().name, 'Table 3')

    def test_delete_a_table(self):
        url = reverse('table_delete', args=(self.table1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ReservationAPITestCase(APITestCase):
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

    def test_get_all_reservations(self):
        url = reverse('reserv_list')
        response = self.client.get(url)
        reservations = Reservation.objects.all()
        serializer_data = ReservationSerializer(reservations, many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_create_a_success_reservation(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 15, 30).isoformat(),
            'duration_minutes': 30
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.all().count(), 3)
        self.assertEqual(Reservation.objects.last().customer_name, 'Петя Иванов')
    
    def test_create_a_reservation_from_10_to_11(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 10).isoformat(),
            'duration_minutes': 60
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_reservation_from_10_10_to_10_50(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 10, 10).isoformat(),
            'duration_minutes': 40
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_reservation_from_9_to_12(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 9).isoformat(),
            'duration_minutes': 180
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_reservation_from_9_to_10_30(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 9).isoformat(),
            'duration_minutes': 90
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_a_reservation_from_10_30_to_11(self):
        url = reverse('reserv_list')
        data = {
            'customer_name': 'Петя Иванов',
            'table_id': self.table1.id,
            'reservation_time': datetime(2025, 10, 1, 10, 30).isoformat(),
            'duration_minutes': 90
            }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_a_reservation(self):
        url = reverse('reserv_delete', args=(self.reservation1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
