import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_car_create(authenticated_boss, authenticated_viewer, car_data):
    url = reverse("cars-list")
    response = authenticated_boss.post(url, car_data, format="json")
    assert response.status_code == 201
    r = authenticated_viewer.get(
        reverse("cars-detail", kwargs={"pk": response.data["id"]})
    )
    assert r.status_code == 404


@pytest.mark.django_db
def test_car_update(authenticated_viewer, authenticated_employee, car_data):
    url = reverse("cars-list")
    response = authenticated_employee.post(url, car_data, format="json")
    assert response.status_code == 201
    url = reverse("cars-detail", kwargs={"pk": response.data["id"]})
    r = authenticated_viewer.put(url, car_data, format="json")
    assert r.status_code == 404


@pytest.mark.django_db
def test_car_detete(authenticated_viewer, authenticated_employee, car_data):
    url = reverse("cars-list")
    response = authenticated_viewer.post(url, car_data, format="json")
    assert response.status_code == 201
    r = authenticated_employee.delete(
        reverse("cars-detail", kwargs={"pk": response.data["id"]})
    )
    assert r.status_code == 204


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_car_list(authenticated_user, user, owner):
    user.owner = owner
    user.save()
    url = reverse("cars-list")
    response = authenticated_user.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_car_create_all(authenticated_user, user, owner, car_data):
    user.owner = owner
    user.save()
    url = reverse("cars-list")
    response = authenticated_user.post(url, car_data, format="json")
    assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_area_list(authenticated_user, user, owner):
    user.owner = owner
    user.save()
    url = reverse("area-list")
    response = authenticated_user.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_area_create(authenticated_user, user, owner, area_data):
    user.owner = owner
    user.save()
    url = reverse("area-list")
    response = authenticated_user.post(url, area_data, format="json")
    if owner == "viewer":
        assert response.status_code == 403
    else:
        assert response.status_code == 201


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_area_update(
    authenticated_user, authenticated_employee, user, owner, area_data
):
    user.owner = owner
    user.save()
    url = reverse("area-list")
    r = authenticated_employee.post(url, area_data, format="json")
    url = reverse("area-detail", kwargs={"pk": r.data["id"]})
    response = authenticated_user.put(url, area_data, format="json")
    if owner == "boss":
        assert response.status_code == 200
    else:
        assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_area_delete(
    authenticated_user, authenticated_employee, user, owner, area_data
):
    user.owner = owner
    user.save()
    url = reverse("area-list")
    r = authenticated_employee.post(url, area_data, format="json")
    url = reverse("area-detail", kwargs={"pk": r.data["id"]})
    response = authenticated_user.delete(url, format="json")
    if owner == "boss":
        assert response.status_code == 204
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_parking_status(authenticated_user, owner, user):
    user.owner = owner
    user.save()
    url = reverse("park-list")
    response = authenticated_user.get(url)
    if owner in ["employee", "boss"]:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_parking_create(authenticated_user, car_id, area_id, owner, user):
    user.owner = owner
    user.save()
    url = reverse("park-list")
    data = {"car": car_id, "area": area_id}
    response = authenticated_user.post(url, data, format="json")
    if owner in ["employee", "boss"]:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_parking_update(authenticated_user, owner, user, parked):
    user.owner = owner
    user.save()
    url = reverse("park-detail", kwargs={"pk": parked})
    response = authenticated_user.put(url)
    if owner in ["employee", "boss"]:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.parametrize("owner", ["viewer", "employee", "boss"])
def test_parking_delete(authenticated_user, owner, user, parked):
    user.owner = owner
    user.save()
    url = reverse("park-detail", kwargs={"pk": parked})
    response = authenticated_user.delete(url)
    if owner in ["employee", "boss"]:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
# @pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_car_len(authenticated_user, car_data):
    url = reverse("cars-list")
    response = authenticated_user.post(url, car_data, format="json")
    assert response.status_code == 201
    r = authenticated_user.get(reverse("cars-list"))
    assert len(r.data) > 0


@pytest.mark.django_db
# @pytest.mark.parametrize('owner',['viewer','employee','boss'])
def test_car_data(authenticated_user, car_data):
    url = reverse("cars-list")
    response = authenticated_user.post(url, car_data, format="json")
    assert response.status_code == 201
    r = authenticated_user.get(
        reverse("cars-detail", kwargs={"pk": response.data["id"]})
    )
    assert r.data["brand"] == car_data["brand"]
