from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.utils.translation import gettext as _

# Create your models here.
# Custom User model inheriting from AbstractUser
class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    points = models.IntegerField(default=0)

    # Custom related_name for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name="%(class)s_groups")
    user_permissions = models.ManyToManyField(Permission, related_name="%(class)s_permissions")

    def __str__(self):
        return self.email



