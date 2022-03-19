import django
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.exceptions import NotFound


def get_object_or_404_json(model,*args, **kwargs):
    try:
        object = model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        raise NotFound(detail=f'{(model._meta.model_name).capitalize()} does not exist.',code=status.HTTP_404_NOT_FOUND)
    return object