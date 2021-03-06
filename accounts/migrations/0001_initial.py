# Generated by Django 3.2.9 on 2021-12-02 09:33

import accounts.utils
import accounts.validators
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('birthday', models.DateField(default='1970-01-01', validators=[accounts.validators.BirthdayValidator(limit_value=18)], verbose_name='Дата рождения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Статус аккаунта')),
                ('activation_key', models.CharField(blank=True, max_length=128)),
                ('activation_key_expires', models.DateTimeField(default=datetime.datetime(2021, 12, 4, 9, 33, 48, 735017, tzinfo=utc))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(blank=True, choices=[('M', 'MAN'), ('W', 'WOMAN')], max_length=10, verbose_name='Пол')),
                ('avatar', models.ImageField(default='default/default.jpg', upload_to=accounts.utils.user_directory_path, verbose_name='Аватар')),
                ('city', models.CharField(max_length=20, verbose_name='Город')),
                ('phone', models.CharField(blank=True, help_text='+7..........', max_length=16, validators=[accounts.validators.RegexValidatorPhone(limit_value='^(\\+(7|1)|8)[0-9]{9}')], verbose_name='Телефон')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'db_table': 'profile',
            },
        ),
    ]
