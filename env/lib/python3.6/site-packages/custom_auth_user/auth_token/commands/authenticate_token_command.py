# -*- coding: utf-8
# Models
from custom_auth_user.models import AuthToken


def authenticate_token(auth_token_store, auth_token):
    try:
        user = auth_token_store.query_set.select_related(
            'user').filter_by_active().find_by_token(auth_token).user

        if user.is_disabled is True:
            return None

        if user.is_active is False:
            return None
    except AuthToken.DoesNotExist:
        return None

    return user
