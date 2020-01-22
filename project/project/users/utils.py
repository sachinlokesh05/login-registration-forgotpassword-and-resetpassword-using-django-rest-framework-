import datetime
from django.conf import settings
from django.utils import timezone
expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def jwt_response_payload_handler(token, user, request=None):
    return {
        'token': token,
        'user': user.username,
        'expire': timezone.now()+expire_delta - datetime.timedelta(seconds=500)
    }
