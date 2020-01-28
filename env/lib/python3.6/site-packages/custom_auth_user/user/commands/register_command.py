# -*- coding: utf-8


def register(user_store, email, username, first_name, last_name, password):
    """
    Register command
    """

    return user_store.create(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password)
