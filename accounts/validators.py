from datetime import date

from django.core.validators import BaseValidator


class BirthdayValidator(BaseValidator):
    message = 'Действует ограничение по возрасту - 18+'

    def compare(self, age, valid_age):
        birthday = age
        today = date.today()
        data = today.year - birthday.year - (
                (today.month, today.day) < (birthday.month, birthday.day))
        return data < valid_age


birthday_validator = BirthdayValidator(limit_value=18)
