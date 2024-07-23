import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from cars.factories.all_factory import *

from faker import Faker

faker=Faker()

User=get_user_model()

def faker_area():
    return f'Area {faker.random_int(min=1,max=800)}'

@pytest.fixture
def user():
    return UserFactory(owner='viewer')
    
@pytest.fixture
def boss():
    return UserFactory(owner='boss')

@pytest.fixture
def viewer():
    return UserFactory(owner='viewer')

@pytest.fixture
def employee():
    return UserFactory(owner='employee')

@pytest.fixture
def authenticated_user(user):
    client=APIClient()
    token=RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client

@pytest.fixture
def authenticated_boss(boss):
    client=APIClient()
    token=RefreshToken.for_user(boss)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client

@pytest.fixture
def authenticated_employee(employee):
    client=APIClient()
    token=RefreshToken.for_user(employee)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client

@pytest.fixture
def authenticated_viewer(viewer):
    client=APIClient()
    token=RefreshToken.for_user(viewer)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client

@pytest.fixture
def car_data():
    data = {
        'brand': faker.company(),
        'color': faker.color_name(),
        'liscence': faker.license_plate(),
        'status': True
    }
    return data

@pytest.fixture
def area_data():
    data = {
        'name': faker_area(),
        'status': True
    }
    return data

@pytest.fixture
def car_id(viewer):
    return CarFactory().id

@pytest.fixture
def area_id():
    return AreaFactory().id

@pytest.fixture
def parked(authenticated_boss,car_id,area_id):
    return ParkingDetailFactory().id