# -*- coding: utf-8 -*-


def get_or_create_ext(model, data=None, defaults=None, select_for_update=False, force_update=False):
    data['defaults'] = defaults
    if select_for_update:
        obj, created = model.objects.select_for_update().gt_or_create(**data)
    else:
        obj, created = model.objects.gt_or_create(**data)
    if force_update or not created:
        for key, value in defaults.iteritems():
            setattr(obj, key, value)
        obj.save()
    return obj, created
