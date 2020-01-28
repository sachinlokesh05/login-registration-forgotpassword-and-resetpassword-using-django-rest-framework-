# -*- coding: utf-8
# Core
from django.contrib import admin

# Model
from custom_auth_user.models import User
from custom_auth_user.models import AuthToken

# Admin
from custom_auth_user.user.admin import UserAdmin
from custom_auth_user.auth_token.admin import AuthTokenAdmin


# Register admins
admin.site.register(User, UserAdmin)
admin.site.register(AuthToken, AuthTokenAdmin)
