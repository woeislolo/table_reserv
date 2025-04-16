import json
from datetime import datetime

from django.urls import reverse
from django.utils import timezone

import pytz

from rest_framework import status

import pytest

from reserv.models import *
from reserv.serializers import *


@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.fixture
def create_db():
    table1 = Table.objects.create(name='Table 1',
                                        seats=4,
                                        location=1)
    table2 = Table.objects.create(name='Table 2',
                                        seats=3,
                                        location=2)
    reservation1 = Reservation.objects.create(customer_name='Петя Иванов',
                                           table_id=table1,
                                           reservation_time=datetime(2025, 10, 1, 10),
                                           duration_minutes=60)
        
    reservation2 = Reservation.objects.create(customer_name='Саша Иванов',
                                           table_id=table1,
                                           reservation_time=datetime(2025, 10, 1, 12, 30),
                                           duration_minutes=90)
    
    return {'table1': table1, 
            'table2': table2, 
            'reservation1': reservation1, 
            'reservation2': reservation2}


@pytest.mark.django_db
def test_get_all_tables(api_client):
    url = reverse('table_list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_a_table(api_client):
    url = reverse('table_list')
    data = {
        'name': 'Table 3',
        'seats': 4,
        'location': 1,
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_delete_a_table(api_client, create_db):
    table2=create_db.get('table2')
    url = reverse('table_delete', args=(table2.id,))
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_get_all_reservations(api_client):
    url = reverse('reserv_list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_a_reservation(api_client, create_db):
    reservation1=create_db.get('reservation1')
    url = reverse('reserv_delete', args=(reservation1.id,))
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_create_a_success_reservation(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 15, 30).isoformat(),
        # 'reservation_time': timezone.datetime(2025, 10, 1, 15, 30, tzinfo=pytz.UTC).isoformat(),
        'duration_minutes': 30
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db  
def test_create_a_reservation_from_10_to_11(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 10).isoformat(),
        'duration_minutes': 60
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_a_reservation_from_10_10_to_10_50(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 10, 10).isoformat(),
        'duration_minutes': 40
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_a_reservation_from_9_to_12(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 9).isoformat(),
        'duration_minutes': 180
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == response.status_code, status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_a_reservation_from_9_to_10_30(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 9).isoformat(),
        'duration_minutes': 90
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == response.status_code, status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_a_reservation_from_10_30_to_11(api_client, create_db):
    url = reverse('reserv_list')
    data = {
        'customer_name': 'Петя Иванов',
        'table_id': create_db.get('table1').id,
        'reservation_time': datetime(2025, 10, 1, 10, 30).isoformat(),
        'duration_minutes': 90
        }
    json_data = json.dumps(data)
    response = api_client.post(url, data=json_data, content_type='application/json')
    assert response.status_code == response.status_code, status.HTTP_400_BAD_REQUEST
