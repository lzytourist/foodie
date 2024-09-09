from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        """
        User roles for providing permissions across applications.
        """
        USER = 'user', 'User'
        OWNER = 'owner', 'Owner'
        EMPLOYEE = 'employee', 'Employee'

    # Roles can be assigned only which are defined in Role class
    # When a user register they are treated as normal user as they have
    # user role assigned to them by default.
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )
