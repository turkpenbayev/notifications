import celery
from logging import getLogger

from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from notifications.utils import ActionError
from notifications.models import Customer, Message, Mailing
from notifications.tasks import notify_client


logger = getLogger('django')


class RemoveCustomer:

    @transaction.atomic()
    def __call__(self, customer_id: int) -> bool:
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise ActionError('Customer does not exist')

        logger.info(
            f'remove pending messages with customer_id={customer_id} from queue')
        task_ids = Message.objects.filter(
            customer_id=customer_id
        ).values_list('task_id', flat=True)
        for task_id in task_ids:
            if task_id is not None:
                celery.control.revoke(task_id, terminate=True)

        customer.delete()


class SendMessages:

    def __call__(self, mailing_id: int) -> None:
        logger.info(f'send message mailing_id={mailing_id}')
        try:
            mailing = Mailing.objects.get(id=mailing_id)
        except Mailing.DoesNotExist:
            raise ActionError('Mailing does not exist')

        customers = Customer.objects.all()
        customers_filter = Q()
        if mailing.filters.phone_code:
            customers_filter = Q(phone_code=mailing.filters.phone_code)
        if mailing.filters.tags:
            tag_filter = Q()
            for tag in mailing.filters.tags:
                tag_filter |= Q(tag__contains=tag)
            customers_filter &= tag_filter

        customers = customers.filter(customers_filter)

        for customer in customers:
            now = timezone.now()
            eta = 0
            send_message = False

            if mailing.start_at <= now <= mailing.end_at:
                eta = None
                send_message = True
            elif now < mailing.start_at < mailing.end_at:
                eta = mailing.start_at
                send_message = True

            if send_message:
                message = Message.objects.create(
                    mailing_id=mailing_id,
                    customer_id=customer.pk
                )
                notify_client.apply_async(
                    args=(message.pk,),
                    eta=eta,
                    task_id=str(message.task_id)
                )
