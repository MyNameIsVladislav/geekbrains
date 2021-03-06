# Generated by Django 3.2.9 on 2021-12-06 10:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.PositiveIntegerField(default=0, verbose_name='money')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'permissions': (('can_add_money', 'Top up balance'),),
                'unique_together': {('user_id', 'id')},
            },
        ),
    ]
