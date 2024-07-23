from django.urls import reverse, resolve
from rest_framework.test import APITestCase,APIClient
from cars.models import Car, AreaName, ParkingDetails
from cars.api.views import CarViewSet, AreaViewSet, ParkViewSet
from rest_framework import status
from django.contrib.auth import get_user_model

User=get_user_model()

class URLTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="admin@gmail.com",
            password="admin",
            phone="9810258171",
            owner="boss"
        )
        self.car = Car.objects.create(
            brand='Toyota',
            color='Red',
            liscence='ABC123',
            status=False,
            owner=self.user
        )
        self.area=AreaName.objects.create(
            name="Area 1",
            status=False
        )
        self.park=ParkingDetails.objects.create(
            car=self.car,
            area=self.area
        )
        self.client=APIClient()
        self.client.force_authenticate(user=self.user)


    def test_car_list_url_resolves_to_correct_view_function(self):
        url = reverse('cars-list')
        self.assertEqual(resolve(url).func.__name__, 'CarViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_car_detail_url_resolves_to_correct_view_function(self):
        url = reverse('cars-detail', kwargs={'pk': self.car.pk})
        # Check the function name in the resolved URL
        self.assertEqual(resolve(url).func.__name__, 'CarViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_area_list_url_resolves_to_correct_view_function(self):
        url = reverse('area-list')
        # Check the function name in the resolved URL
        self.assertEqual(resolve(url).func.__name__, 'AreaViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_area_detail_url_resolves_to_correct_view_function(self):
        url = reverse('area-detail', kwargs={'pk': self.area.pk})
        # Check the function name in the resolved URL
        self.assertEqual(resolve(url).func.__name__, 'AreaViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_park_list_url_resolves_to_correct_view_function(self):
        url = reverse('park-list')
        # Check the function name in the resolved URL
        self.assertEqual(resolve(url).func.__name__, 'ParkViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_park_detail_url_resolves_to_correct_view_function(self):
        url = reverse('park-detail', kwargs={'pk': self.park.pk})
        # Check the function name in the resolved URL
        self.assertEqual(resolve(url).func.__name__, 'ParkViewSet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
