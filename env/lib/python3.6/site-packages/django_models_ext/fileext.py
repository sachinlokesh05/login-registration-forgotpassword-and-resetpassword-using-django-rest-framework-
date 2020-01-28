# -*- coding: utf-8 -*-

import os

from django.conf import settings
from TimeConvert import TimeConvert as tc


def upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/file/<ym>/<stamp>.<ext>
    return 'file/{ym}/{stamp}{ext}'.format(
        ym=tc.local_string(format='%Y%m'),
        stamp=tc.local_timestamp(ms=True),
        ext=os.path.splitext(filename)[1].lower(),
    )


def upload_file_url(image_field_file):
    return image_field_file and ('{0}{1}'.format(settings.DOMAIN if hasattr(settings, 'DOMAIN') else '', image_field_file.url)) or ''


def upload_file_path(image_field_file):
    return image_field_file and image_field_file.name or ''


def upload_file_store_path(image_field_file):
    return image_field_file and image_field_file.path or ''
