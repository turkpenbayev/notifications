import requests
from logging import getLogger

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
            response = session.post(
                url=f'https://probe.fbrq.cloud/v1/send/{message_id}',
                json=data,
                headers={
                    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDEzNDI1ODEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6InR1cmtwZW5iYXlldiJ9.zrl13SbkhE-H22_bvUd9tDrWOIuOl1zir_QySksU_Cs'
                }
            )
            response.raise_for_status()
        except requests.RequestException as e:
            logger.warning(e)
            return Message.Status.FAILURE

        return Message.Status.SUCCESS
