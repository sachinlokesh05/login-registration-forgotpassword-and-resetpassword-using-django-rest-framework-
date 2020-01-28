#!/usr/bin/env python
# -*- coding: utf-8
# Core
from custom_auth_user.auth_token.store import AuthTokenStore


def delete_expired_token(auth_token_store=AuthTokenStore()):
    expired_token = auth_token_store.query_set.filter_by_expired()
    expired_token.delete()


delete_expired_token()
