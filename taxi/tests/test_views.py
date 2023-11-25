from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


def get_user_model_function():
    return get_user_model().objects.create_user(
        username="driver",
        password="password1",
        license_number="ABC12345",
    )


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password",
        )
        self.client.force_login(self.admin_user)

        self.driver = get_user_model_function()

    def test_driver_license_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_detail_license_listed(self) -> None:
        url = reverse(
            "admin:taxi_driver_change", args=[self.driver.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.driver.license_number)

    def test_driver_add_fieldsets(self) -> None:
        url = reverse("admin:taxi_driver_add")
        res = self.client.get(url)
        expected_fields = ["first_name", "last_name", "license_number"]

        for field in expected_fields:
            self.assertContains(res, field)
