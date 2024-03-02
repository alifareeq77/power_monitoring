from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    # @property
    # def get_dashboard(self):
    #     try:
    #         dashboard = UserDashboard.objects.get(user_id=self.id).dashboard_link
    #         return dashboard
    #     except UserDashboard.DoesNotExist:
    #         return None
