import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model
from cars.models import *
from rest_framework import status


User=get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="admin@gmail.com",
        phone="980000032",
        password="admin123",
        owner="viewer"
    )
@pytest.fixture
def boss():
    return User.objects.create_user(
        email="boss@gmail.com",
        phone="9800000",
        password="admin123",
        owner="boss"
    )

@pytest.fixture
def viewer():
    return User.objects.create_user(
        email="viewer@gmail.com",
        phone="980000011",
        password="admin123",
        owner="viewer"
    )

@pytest.fixture
def employee():
    return User.objects.create_user(
        email="employee@gmail.com",
        phone="9811111",
        password="admin123",
        owner="employee"
    )
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
        'brand': 'Honda',
        'color': 'Blue',
        'liscence': 'XYZ987',
        'status': True
    }
    return data

@pytest.fixture
def area_data():
    data = {
        'name': 'Area 1',
        'status': True
    }
    return data

@pytest.fixture
def car_id(viewer):
    car=Car.objects.create(
        brand= 'Honda',
        color= 'Blue',
        liscence= 'XYZ987',
        status= False,
        owner=viewer
    )
    return car.id

@pytest.fixture
def area_id():
    area=AreaName.objects.create(
        name='Area 67',
        status=False
    )
    return area.id

@pytest.fixture
def parked(authenticated_boss,car_id,area_id):
    url=reverse('park-list')
    data = {
        'car':car_id,
        'area':area_id
    }
    response=authenticated_boss.post(url,data,format='json')
    assert response.status_code == status.HTTP_201_CREATED
    return response.data['id']

@pytest.mark.django_db
def test_car_create(authenticated_boss,authenticated_viewer,car_data):
    url=reverse('cars-list')
    response=authenticated_boss.post(url,car_data,format='json')
    assert response.status_code==201
    r = authenticated_viewer.get(reverse('cars-detail', kwargs={'pk':response.data["id"]}))
    assert r.status_code==404


@pytest.mark.django_db
def test_car_updates(authenticated_viewer,authenticated_employee,car_data):
    url=reverse('cars-list')
    response=authenticated_employee.post(url,car_data,format='json')
    assert response.status_code==201
    url=reverse('cars-detail', kwargs={'pk':response.data["id"]})
    # r = authenticated_viewer.put(url,car_data,format='json')
    r=authenticated_viewer.get(reverse('cars-list'))
    print(r.data)
    assert r.status_code==200

@pytest.mark.django_db
def test_car_detete(authenticated_viewer,authenticated_employee,car_data):
    url=reverse('cars-list')
    response=authenticated_viewer.post(url,car_data,format='json')
    assert response.status_code==201
    r = authenticated_employee.delete(reverse('cars-detail', kwargs={'pk':response.data["id"]}))
    assert r.status_code==204

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_car_list(authenticated_user,user,owner):
    user.owner=owner
    user.save()
    url = reverse('cars-list')
    response=authenticated_user.get(url)
    assert response.status_code==200

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_car_create_all(authenticated_user,user,owner,car_data):
    user.owner=owner
    user.save()
    url = reverse('cars-list')
    response=authenticated_user.post(url,car_data,format='json')
    assert response.status_code==201

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_area_list(authenticated_user,user,owner):
    user.owner=owner
    user.save()
    url = reverse('area-list')
    response=authenticated_user.get(url)
    assert response.status_code==200

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_area_create(authenticated_user,user,owner,area_data):
    user.owner=owner
    user.save()
    url = reverse('area-list')
    response=authenticated_user.post(url,area_data,format='json')
    if owner=='viewer':
        assert response.status_code==403
    else:
        assert response.status_code==201

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_area_update(authenticated_user,authenticated_employee,user,owner,area_data):
    user.owner=owner
    user.save()
    url=reverse('area-list')
    r=authenticated_employee.post(url,area_data,format='json')
    url = reverse('area-detail', kwargs={'pk':r.data["id"]})
    response=authenticated_user.put(url,area_data,format='json')
    if owner=='boss':
        assert response.status_code==200
    else:
        assert response.status_code==403

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_area_delete(authenticated_user,authenticated_employee,user,owner,area_data):
    user.owner=owner
    user.save()
    url=reverse('area-list')
    r=authenticated_employee.post(url,area_data,format='json')
    url = reverse('area-detail', kwargs={'pk':r.data["id"]})
    response=authenticated_user.delete(url,format='json')
    if owner=='boss':
        assert response.status_code==204
    else:
        assert response.status_code==status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_parking_status(authenticated_user,owner,user):
    user.owner=owner
    user.save()
    url=reverse('park-list')
    response=authenticated_user.get(url)
    if owner in ['employee','boss']:
        assert response.status_code==status.HTTP_200_OK
    else:
        assert response.status_code==status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_parking_create(authenticated_user,car_id,area_id,owner,user):
    user.owner=owner
    user.save()
    url=reverse('park-list')
    data={
        'car':car_id,
        'area':area_id
    }
    response=authenticated_user.post(url,data,format='json')
    if owner in ['employee','boss']:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_parking_update(authenticated_user,owner,user,parked):
    user.owner=owner
    user.save()
    url=reverse('park-detail',kwargs={'pk':parked})
    response=authenticated_user.put(url)
    if owner in ['employee','boss']:
        assert response.status_code==status.HTTP_200_OK
    else:
        assert response.status_code==status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
@pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_parking_delete(authenticated_user,owner,user,parked):
    user.owner=owner
    user.save()
    url=reverse('park-detail',kwargs={'pk':parked})
    response=authenticated_user.delete(url)
    if owner in ['employee','boss']:
        assert response.status_code==status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code==status.HTTP_403_FORBIDDEN