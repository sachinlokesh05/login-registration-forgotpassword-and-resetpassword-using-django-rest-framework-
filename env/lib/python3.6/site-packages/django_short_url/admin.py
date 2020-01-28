# -*- coding: utf-8 -*-

from django.contrib import admin
from django_admin import DeleteOnlyModelAdmin
from django_short_url.models import ShortURL


class ShortURLAdmin(DeleteOnlyModelAdmin, admin.ModelAdmin):
    list_display = ('surl', 'lurl', 'status', 'created_at', 'updated_at')


admin.site.register(ShortURL, ShortURLAdmin)
