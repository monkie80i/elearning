import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet,Model
from rest_framework import status
from rest_framework.exceptions import NotFound


def get_object_or_404_json(thing,*args, **kwargs):
    try:
        if type(thing) == type(Model):
            object = thing.objects.get(**kwargs)
        elif type(thing) == QuerySet:
            object = thing.get(**kwargs)
    except ObjectDoesNotExist:
        raise NotFound(detail=f'{(thing._meta.model_name).capitalize()} does not exist.',code=status.HTTP_404_NOT_FOUND)
    return object