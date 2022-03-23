from rest_framework import serializers
from .serializers import *
from drf_yasg import openapi
# these are only for schema generation in documentation

CourseCreateRequest = openapi.Schema(
    title='Course Create',
    description='Create a Course . Requires login.',
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(
            title="Course Title",
            type=openapi.TYPE_STRING,
        ),
        'overview': openapi.Schema(
            title="Course Overview",
            type=openapi.TYPE_STRING,
        ),
        'subject_slug': openapi.Schema(
            title="Slug of the subject",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_SLUG,
            pattern=r'^[-a-zA-Z0-9_]+$',
        )
    },
    required=['title','overview','subject_slug'],
    )

