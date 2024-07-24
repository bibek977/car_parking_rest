from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from cars.models import *

User = get_user_model()


class CarViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="admin@gmail.com", password="admin", phone="9810258171", owner="boss"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.car = Car.objects.create(
            brand="Toyota",
            color="Red",
            liscence="ABC123",
            status=False,
            owner=self.user,
        )
        self.area = AreaName.objects.create(name="Area 1", status=False)
        self.car_url = reverse("cars-list")
        self.car_detail_url = reverse("cars-detail", args=[self.car.id])

    def test_car_list(self):
        response = self.client.get(self.car_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Toyota", str(response.data))
        self.assertTrue(len(response.data) == 1)

    def test_car_create(self):

        data = {"brand": "Honda", "color": "Blue",
                "liscence": "XYZ987", "status": True}
        response = self.client.post(self.car_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Car.objects.filter(liscence="XYZ987").exists())
        self.assertFalse(Car.objects.filter(
            liscence="XYZ987").exists() is None)
        self.assertEqual(
            Car.objects.filter(liscence="XYZ987").first(
            ).owner.email, "admin@gmail.com"
        )

    def test_car_create_user(self):
        viewer = User.objects.create(
            email="viewer@gmail.com", password="admin", phone="1", owner="viewer"
        )
        self.client.force_authenticate(user=viewer)
        data = {"brand": "Honda", "color": "Blue",
                "liscence": "XYZ987", "status": True}
        response = self.client.post(self.car_url, data)
        r = self.client.get(self.car_url)

        self.assertIn("Honda", str(response.data))
        self.assertFalse(Car.objects.filter(
            liscence="XYZ987").exists() is None)

    def test_car_update(self):
        data = {
            "brand": "Honda",
            "color": "Green",
            "liscence": "ABC123",
            "status": False,
        }
        response = self.client.put(self.car_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.car.refresh_from_db()
        self.assertEqual(self.car.color, "Green")

    def test_car_delete(self):
        response = self.client.delete(self.car_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())


class AreaViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="admin@gmail.com", password="admin", phone="9810258171", owner="boss"
        )
        self.viewer = User.objects.create(
            email="viewer@gmail.com", password="admin", phone="988171", owner="viewer"
        )
        self.employee = User.objects.create(
            email="employee@gmail.com",
            password="admin",
            phone="9881711111",
            owner="employee",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.car = Car.objects.create(
            brand="Toyota",
            color="Red",
            liscence="ABC123",
            status=False,
            owner=self.user,
        )
        self.area = AreaName.objects.create(name="Area 1", status=False)
        self.area_url = reverse("area-list")
        self.area_detail_url = reverse("area-detail", args=[self.area.id])

    def test_list_area(self):
        response = self.client.get(self.area_url)
        self.assertEqual(response.status_code, 200)

    def test_create_area(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Area 3", "status": False}
        response = self.client.post(self.area_url, data)
        self.assertEqual(response.status_code, 201)

    def test_create_area_viewer(self):
        self.client.force_authenticate(user=self.viewer)
        data = {"name": "Area 7", "status": False}
        response = self.client.post(self.area_url, data)
        self.assertEqual(response.status_code, 403)

    def test_area_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.area_detail_url)
        self.assertEqual(response.status_code, 204)

    def test_area_delete_viewer(self):
        self.client.force_authenticate(user=self.viewer)
        response = self.client.delete(self.area_detail_url)
        self.assertEqual(response.status_code, 403)


class ParkingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="admin@gmail.com", password="admin", phone="9810258171", owner="boss"
        )
        self.viewer = User.objects.create(
            email="viewer@gmail.com", password="admin", phone="988171", owner="viewer"
        )
        self.employee = User.objects.create(
            email="employee@gmail.com",
            password="admin",
            phone="9881711111",
            owner="employee",
        )
        # self.client=APIClient()
        # self.client.force_authenticate(user=self.user)

        self.car = Car.objects.create(
            brand="Toyota",
            color="Red",
            liscence="ABC123",
            status=False,
            owner=self.user,
        )
        self.area = AreaName.objects.create(name="Area 1", status=False)
        self.park = ParkingDetails.objects.create(car=self.car, area=self.area)
        self.park_url = reverse("park-list")
        self.park_detail_url = reverse("park-detail", args=[self.park.id])
        self.car_url = reverse("cars-list")
        self.car_detail_url = reverse("cars-detail", args=[self.car.id])

    def test_list_parking(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.employee)
        response = self.client.get(self.park_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(self.park_detail_url)
        self.assertEqual(response.status_code, 200)

    def test_list_parking_viewer(self):
        v = User.objects.create(
            email="new@gmail.com", password="admin", phone="0258171", owner="viewer"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.viewer)
        response = self.client.get(self.park_url)
        # print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_create_parking(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.viewer)
        car_new = Car.objects.create(
            brand="Toyota",
            color="Blue",
            liscence="XYZ789",
            status=False,
            owner=self.viewer,
        )
        area_new = AreaName.objects.create(name="Area 54", status=False)
        park_new = {"car": car_new.id, "area": area_new.id}
        response = self.client.post(self.park_url, park_new)
        self.assertEqual(response.status_code, 403)
        # self.assertEqual(response.status_code,204)

    def test_delete_parking(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.employee)
        response = self.client.delete(self.park_detail_url)
        self.assertEqual(response.status_code, 204)
        # self.assertEqual(response.status_code,403)

    def test_update_parking(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.employee)
        response = self.client.put(self.park_detail_url)
        # self.assertEqual(response.status_code,403)
