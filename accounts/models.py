from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from accounts.managers import CustomUserManager
from accounts.validators import birthday_validator


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Email', unique=True)
    birthday = models.DateField(verbose_name='Дата рождения', validators=[birthday_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthday']

    objects = CustomUserManager()

    # для отправки почты при регистрации
    activation_key = models.CharField(
        max_length=128,
        blank=True
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48))
    )

    def is_activation_key_expired(self):
        return False if now() <= self.activation_key_expires else True

    def __str__(self):
        return self.email
