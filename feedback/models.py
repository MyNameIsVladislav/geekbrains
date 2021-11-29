from django.db import models


class FeedBack(models.Model):
    """ Модель для приема заявок на обратную связь """
    first_name = models.CharField(verbose_name='Имя', max_length=20)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Комментарий пользователя')

    status_request = models.BooleanField(verbose_name='Статус заявки', default=False)  # True - заявка обработана

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
