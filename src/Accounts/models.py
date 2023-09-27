from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.apps import apps

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not password:
            raise ValueError("No password was provided")
        # email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        # username = GlobalUserModel.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name, last_name=last_name, **extra_fields)
        user.password = make_password(password)
        print(user.password)
        user.save(using=self._db)
        return user
    

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, first_name, last_name, **extra_fields)


class CustomUserModel(AbstractUser):
    email = models.EmailField(("email"), unique=True)
    password = models.CharField(("password"), max_length=128)
    username = models.CharField(max_length=128, blank=True, unique=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
