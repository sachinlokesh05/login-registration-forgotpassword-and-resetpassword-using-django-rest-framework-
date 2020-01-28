# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_models_ext import BaseModelMixin


class ShortURL(BaseModelMixin):
    surl = models.CharField(_(u'surl'), max_length=32, blank=True, null=True, help_text=u'短链', db_index=True, unique=True)
    lurl = models.CharField(_(u'lurl'), max_length=255, blank=True, null=True, help_text=u'长链', db_index=True, unique=True)

    class Meta:
        verbose_name = _(u'shorturl')
        verbose_name_plural = _(u'shorturl')

    def __unicode__(self):
        return unicode(self.pk)

    @property
    def fdomain(self):
        if hasattr(settings, 'DJANGO_SHORT_URL_DOMAIN'):
            return settings.DJANGO_SHORT_URL_DOMAIN
        elif hasattr(settings, 'DOMAIN'):
            return settings.DOMAIN
        return ''

    def fsurl(self, domain=None, regex='s'):
        return u'{0}/{1}/{2}'.format(domain or self.fdomain, regex, self.surl)

    @property
    def data(self):
        return {
            'lurl': self.lurl,
            'surl': self.fsurl,
        }
