# -*- coding: utf-8 -*-

import shortuuid
from CodeConvert import CodeConvert as cc
from django.conf import settings
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django_short_url.models import ShortURL
from furl import furl


def short_url_redirect(request, surl):
    """
    >> Chrome 请求
    ?nickname=姜戈

    >> Django 获取
    u'?nickname=%E5%A7%9C%E6%88%88'

    >> furl(lurl).add(furl(request.get_raw_uri()).query.params).url
    ?nickname=%C3%A5%C2%A7%C2%9C%C3%A6%C2%88%C2%88

    >> furl(lurl).add(furl(cc.Convert2Utf8(request.get_raw_uri())).query.params).url
    ?nickname=%E5%A7%9C%E6%88%88
    """
    try:
        lurl = ShortURL.objects.get(surl=surl).lurl
    except ShortURL.DoesNotExist:
        lurl = None

    # Short URL Not Exists
    if not lurl:
        redirect_url = ''

        if hasattr(settings, 'DJANGO_SHORT_URL_REDIRECT_URL'):
            redirect_url = settings.DJANGO_SHORT_URL_REDIRECT_URL

        if hasattr(settings, 'DJANGO_SHORT_URL_FUNC') and hasattr(settings.DJANGO_SHORT_URL_FUNC, '__call__'):
            redirect_url = settings.DJANGO_SHORT_URL_FUNC(request)

        if not redirect_url:
            return render(request, 'django_short_url/errmsg.html', {'title': 'Error', 'errmsg': 'Short URL not Exists'})

        return redirect(redirect_url)

    return redirect(furl(lurl).add(furl(cc.Convert2Utf8(request.get_raw_uri())).query.params).url)


def get_surl(lurl, length=None, domain=None, regex='s'):
    sobj, created = ShortURL.objects.get_or_create(lurl=lurl)
    if not sobj.surl:
        length = length or (getattr(settings, 'DJANGO_SHORT_URL_LENGTH') if hasattr(settings, 'DJANGO_SHORT_URL_LENGTH') else 0) or 22
        while True:
            sobj.surl = shortuuid.ShortUUID().random(length=length)
            try:
                sobj.save()
                break
            except IntegrityError:  # IntegrityError: (1062, "Duplicate entry 'xxx' for key 'surl'")
                continue
    return sobj.fsurl(domain=domain, regex=regex)
