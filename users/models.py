from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    custom user model with email login
    """

    OWNER_CHOICES = (
        ("viewer", _("viewer")),
        ("employee", _("employee")),
        ("boss", _("boss")),
    )  # noqa
    email = models.EmailField(_("email"), unique=True)
    phone = models.CharField(_("phone"), unique=True, max_length=100)
    name = models.CharField(_("full_name"), max_length=100, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    owner = models.CharField(
        max_length=50, choices=OWNER_CHOICES, default="viewer", verbose_name=_("Owner")
    )  # noqa

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
