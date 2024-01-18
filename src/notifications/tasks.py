import uuid
from celery import shared_task
from logging import getLogger

from django.db.models import F
from django.core.mail import send_mail

from notifications.models import Message
from notifications.utils import ActionError
from notifications.services import make_request


logger = getLogger('django')


@shared_task(bind=True)
def notify_client(self, message_id: int):
    status = Message.Status.STARTED
    try:
        message = Message.objects.annotate(
            phone=F('customer__phone'),
            text=F('mailing__text')
        ).get(pk=message_id)
    except Message.DoesNotExist as e:
        logger.error(e)
        raise ActionError(f'Message does not found id={message_id}')
    logger.info(f'sending message to {message.customer_id}')
    status = make_request(message.pk, message.phone, message.text)
    message.status = status
    message.save(update_fields=['status'])
    return
