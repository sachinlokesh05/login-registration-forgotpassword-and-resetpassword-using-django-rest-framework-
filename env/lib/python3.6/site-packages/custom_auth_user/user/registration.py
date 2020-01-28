# -*- coding: utf-8
# Exception
from custom_auth_user.user.exceptions import InvalidInput

# Store
from custom_auth_user.user.store import UserStore

# Forms
from custom_auth_user.user.forms.registration_form import RegistrationForm

# Commands
from custom_auth_user.user.commands.register_command import register


class RegistrationService():
    """
    Registration domain service
    """

    user_store = UserStore()

    def __init__(self, email, username, first_name, last_name, password):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

        # Registration form
        self.registration_form = RegistrationForm(
            user_store=self.user_store,
            data={
                'email': email,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
            })

    def run(self):
        # Validate form
        if not self.registration_form.is_valid():
            raise InvalidInput

        user_data = self.registration_form.cleaned_data

        # Run and return register command
        return register(
            user_store=self.user_store,
            email=user_data.get('email'),
            username=user_data.get('username'),
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            password=user_data.get('password'))

    def get_registration_form_errors(self):
        return self.registration_form.errors
