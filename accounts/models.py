from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from accounts.managers import CustomUserManager
from accounts.validators import birthday_validator, phone_validator
from accounts.utils import user_directory_path


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Email', unique=True)
    birthday = models.DateField(verbose_name='Дата рождения', validators=[birthday_validator], default='1970-01-01')
    is_active = models.BooleanField(default=True, verbose_name='Статус аккаунта')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

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


class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    RU = 'RU'
    EN = 'EN'

    GENDER_CHOICES = (
        (MALE, 'MAN'),
        (FEMALE, 'WOMAN'),
    )

    user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    gender = models.CharField(verbose_name='Пол', max_length=10, choices=GENDER_CHOICES, blank=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to=user_directory_path, default='default/default.jpg')
    city = models.CharField(verbose_name='Город', max_length=20)
    phone = models.CharField(verbose_name='Телефон', validators=[phone_validator],
                             max_length=16, blank=True, help_text='+7..........')

    class Meta:
        db_table = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль пользователя: {self.user.email} - {self.user.id}'

    @property
    def age(self):
        if self.user.birthday:
            today = now()
            return today.year - self.user.birthday.year - (
                    (today.month, today.day) < (self.user.birthday.month, self.user.birthday.day))
        return 0

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
