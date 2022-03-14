from weakref import proxy
from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class CustomUserManager(BaseUserManager):
    '''This class aims to managed our CustomUser.'''

    def create_user(self, first_name, last_name, email, password=None):
        """
        Creates and saves a User with the given email , first_name,
        last_name and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.admin = False
        user.staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        """
        Creates and saves a superuser with the given email , first_name,
        last_name and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)  # change password to hash
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    '''This class aims to defined our own customized user.'''

    class Type(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        SALER = "SALER", "Saler"
        TECHNICIAN = "TECHNICIAN", "Technician"

    type = models.CharField('Type', max_length=50, choices=Type.choices)

    first_name = models.CharField(
        verbose_name='first name',
        max_length=255)
    last_name = models.CharField(
        verbose_name='last name',
        max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    # Since Email & Password are required by default,
    # there's no need to add in REQUIRED_FIELDS.
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return f"{self.email}"

    @staticmethod
    def has_perm(perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return False

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff


class ManagerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Type.MANAGER)


class SalerManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Type.SALER)


class TechnicianManager(CustomUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=CustomUser.Type.TECHNICIAN)


class Manager(CustomUser):
    objects = ManagerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Type.MANAGER
            self.admin = True
        return super().save(*args, **kwargs)


class Saler(CustomUser):
    objects = SalerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Type.SALER
            self.admin = False
        return super().save(*args, **kwargs)


class Technician(CustomUser):
    objects = TechnicianManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = CustomUser.Type.TECHNICIAN
            self.admin = False
        return super().save(*args, **kwargs)
