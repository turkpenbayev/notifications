import requests
from logging import getLogger

from django.conf import settings

from notifications.models import Message


logger = getLogger('django')


def make_request(message_id: int | str, phone: str, text: str) -> int:
    with requests.Session() as session:
        try:
            data = {
                'id': message_id,
                'phone': phone,
                'text': text
            }
            logger.info(f'sending message with id {message_id}, phone: {phone}, text: {text}')
            response = session.post(
                url=f'https://probe.fbrq.cloud/v1/send/{message_id}',
                json=data,
                headers={
                    'Authorization': f'Bearer {settings.SERVICE_JWT_TOKEN}'
                }
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(e)
            return Message.Status.FAILURE

        return Message.Status.SUCCESS
