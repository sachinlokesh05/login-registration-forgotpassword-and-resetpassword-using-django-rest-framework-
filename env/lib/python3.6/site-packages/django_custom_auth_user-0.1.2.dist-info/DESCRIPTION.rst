Django Custom Auth User
=======================

.. image:: https://travis-ci.org/anthon-alindada/django_custom_auth_user.svg?branch=master
    :target: https://travis-ci.org/anthon-alindada/django_custom_auth_user

.. image:: https://codecov.io/gh/anthon-alindada/django_custom_auth_user/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/anthon-alindada/django_custom_auth_user

Django custom user model and abstract user model basic token authentication.

Documentation
-------------

The full documentation is at https://django_custom_auth_user.readthedocs.io.

Features
--------
* Custom user
* Extendable abstract user
* User registration service
* Token authentication
* Create auth token
* Delete auth token
* Query sets for ``User`` & ``AuthToken``

Quickstart
----------

Install Django custom user::

    pip install django_custom_auth_user


Add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'custom_auth_user',
        ...
    )

Set your ``AUTH_USER_MODEL`` setting to use ``custom_auth_user.User``::

    AUTH_USER_MODEL = 'custom_auth_user.User'

Create the database tables::

    python manage.py migrate


Version 0.1 (2017-07-23)
~~~~~~~~~~~~~~~~~~~~~~~~

- Initial release.


