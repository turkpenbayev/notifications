from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class PhoneNumberValidator(RegexValidator):
    """ Phone number validator

    Validates phone number via regular expression
    """

    def __init__(self, message=None):
        super(PhoneNumberValidator, self).__init__(
            regex=r'^(7)\d{10}$',
            message=message or "номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)",
            code='invalid_phone'
        )
