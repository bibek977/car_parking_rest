from django.test import TestCase
from cars.models import Car, AreaName, ParkingDetails
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()

class TestModel(TestCase):
    
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="admin@gmail.com",
            password="admin", 
            phone="9810258171",
            owner="boss"
        )
        self.car = Car.objects.create(
            brand="Tesla",
            color="red",
            liscence="Na2kha2324",
            status=False,
            owner=self.user
        )
        self.area = AreaName.objects.create(
            name="Area 1",
            status=False
        )

    def test_car_creation(self):
        self.assertEqual(self.car.brand, 'Tesla')
        self.assertEqual(self.car.owner, self.user)
        self.assertFalse(self.car.status)

    def test_area_creation(self):
        self.assertEqual(self.area.name, 'Area 1')
        self.assertFalse(self.area.status)

    def test_parking_details(self):
        parking = ParkingDetails.objects.create(
            car=self.car,
            area=self.area,
            status=True
        )
        self.assertEqual(parking.car, self.car)
        self.assertEqual(parking.area, self.area)
        self.assertTrue(parking.status)
        self.assertFalse(self.car.status) 
        self.assertFalse(self.area.status) 
        self.assertIsNotNone(parking.checked_in)
        self.assertIsNone(parking.checked_out)

    def test_parked_in(self):
        parking = ParkingDetails.objects.create(
            car=self.car,
            area=self.area,
            status=True
        )
        self.area.refresh_from_db()
        self.car.refresh_from_db()

        self.assertTrue(self.car.status)
        self.assertTrue(self.area.status)

    def test_area_str(self):
        self.assertEqual(str(self.area), "Area 1")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Na2kha2324")

    def test_parked_in_str(self):
        parking = ParkingDetails.objects.create(
            car=self.car,
            area=self.area,
            status=True
        )
        self.assertEqual(str(parking), "Na2kha2324 : Area 1")

    def test_car_unique_liscense(self):
        with self.assertRaises(IntegrityError):
            Car.objects.create(
                brand='Honda',
                color='Blue',
                liscence='Na2kha2324',  # This should be unique
                status=False,
                owner=self.user
            )

    def test_area_in_parking(self):
        parking = ParkingDetails.objects.create(
            car=self.car,
            area=self.area,
            status=True
        )
        self.assertIn(parking, self.area.areas.all())
        self.assertIn(parking, self.car.liscences.all())