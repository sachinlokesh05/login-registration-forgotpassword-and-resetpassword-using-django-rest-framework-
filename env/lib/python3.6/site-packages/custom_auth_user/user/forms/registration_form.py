# -*- coding: utf-8
# pylint: disable=W0104
# Django
from django import forms

# Models
from django.contrib.auth import get_user_model


class RegistrationForm(forms.Form):
    """
    Registration form
    """

    def __init__(self, user_store, *args, **kwargs):
        self.user_store = user_store
        super(RegistrationForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        max_length=255,
        error_messages={
            'required': 'Email address is required',
            'invalid': 'Email address is invalid'
        })

    username = forms.RegexField(
        regex=r'^[a-z0-9._-]+$',
        error_messages={
            'required': 'Username is required',
            'invalid': 'Usernames can only contain lowercase letters, \
                numbers, periods, hyphens, and underscores'
        })

    first_name = forms.CharField(
        error_messages={
            'required': 'First name is required',
        })

    last_name = forms.CharField(
        error_messages={
            'required': 'Last name is required',
        })

    password = forms.CharField(
        min_length=6,
        error_messages={
            'required': 'Password is required',
            'min_length': 'Password must be at least 6 characters'
        })

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            self.user_store.query_set.find_by_email(email=email)
            raise forms.ValidationError('Email address is already being used')
        except get_user_model().DoesNotExist:
            pass

        return email

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            self.user_store.query_set.find_by_username(username=username)
            raise forms.ValidationError('Username is already being used')
        except get_user_model().DoesNotExist:
            pass

        return username
