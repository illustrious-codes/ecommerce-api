from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.utils.translation import gettext as _

class CustomUserManager(UserManager):

    def __create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email=email)
        user = self.model(email, password, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be have is_staff = True ")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be have is_superuser = True ")
        return self._create_user(email, password, **extra_fields)
    
class User(AbstractUser):

    email = models.EmailField(_("Email"), unique=True, max_length=50, blank=True)
    is_verified = models.BooleanField(_("Is_Verifield"), default=False)
    objects = CustomUserManager()
    EMAIL_FIELD = "email"

    def _str_(self):
        return self.get_full_name() or self.email
