import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# create a custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password=None):
        user = self.create_user(email, first_name, last_name, phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# extend user model from abstract user
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']

    def __str__(self):
        return self.first_name
