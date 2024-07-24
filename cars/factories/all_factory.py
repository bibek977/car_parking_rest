import datetime

import factory
from django.contrib.auth import get_user_model
from django.utils import timezone
from factory.django import DjangoModelFactory
from faker import Faker

from cars.models import *

faker = Faker()

User = get_user_model()


def generate_area_name():
    return f"Area {faker.random_int(min=1, max=100)}"


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    owner = factory.Faker("random_element", elements=[
                          "viewer", "employee", "boss"])
    is_staff = False
    is_active = True
    date_joined = factory.Faker(
        "date_time_this_decade", tzinfo=datetime.timezone.utc)
    last_login = factory.Faker(
        "date_time_this_year", tzinfo=datetime.timezone.utc)


class CarFactory(DjangoModelFactory):
    class Meta:
        model = Car

    brand = factory.Faker("company")
    color = factory.Faker("color_name")
    liscence = factory.Faker("license_plate")
    status = False
    owner = factory.SubFactory(UserFactory)


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = AreaName

    # name = factory.LazyFunction(generate_area_name)
    name = factory.Sequence(lambda n: f"Area {n+1}")
    status = False


class ParkingDetailFactory(DjangoModelFactory):
    class Meta:
        model = ParkingDetails

    car = factory.SubFactory(CarFactory)
    area = factory.SubFactory(AreaFactory)
    status = True
    checked_in = factory.Faker(
        "date_time_this_year",
        before_now=True,
        after_now=False,
        tzinfo=datetime.timezone.utc,
    )
    checked_out = None
