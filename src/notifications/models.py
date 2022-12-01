import json
import pytz
import uuid
from typing import List
from dataclasses import dataclass


from django.db import models

from notifications.validators import PhoneNumberValidator


@dataclass
class MailingFilter:
    phone_code: str | None = None
    tags: List[str] | None = None


class Mailing(models.Model):
    start_at = models.DateTimeField()
    text = models.TextField()
    filter_by = models.TextField()
    end_at = models.DateTimeField()

    @property
    def filters(self) -> MailingFilter:
        return MailingFilter(**json.loads(self.filter_by)) if self.filter_by else MailingFilter()


class Customer(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    validate_phone = PhoneNumberValidator()

    phone = models.CharField(max_length=11, validators=[validate_phone, ], unique=True, null=True,
                             blank=True, error_messages={'unique': 'Phone should be unique'})
    phone_code = models.CharField(max_length=3)
    tag = models.TextField()
    timezone = models.CharField(
        max_length=32, choices=TIMEZONES, default='UTC')


class Message(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 0, 'PENDING'
        STARTED = 1, 'STARTED'
        SUCCESS = 2, 'SUCCESS'
        FAILURE = 3, 'FAILURE'

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(
        choices=Status.choices, default=Status.PENDING)
    mailing = models.ForeignKey(
        'notifications.Mailing', on_delete=models.CASCADE, related_name='messages')
    customer = models.ForeignKey(
        'notifications.Customer', on_delete=models.CASCADE, related_name='messages')
    task_id = models.UUIDField(default=uuid.uuid4, editable=False)
