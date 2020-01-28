# -*- coding: utf-8


def create_auth_token(auth_token_store, user):
    return auth_token_store.create(user)
