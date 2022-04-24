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



text_content_resp = openapi.Schema(
    title=f'Text Content',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            title="Content id",
            type=openapi.TYPE_NUMBER,
        ),
        'order': openapi.Schema(
            title="Content order within parent module",
            type=openapi.TYPE_NUMBER,
        ),
        'module': openapi.Schema(
            title="Perent module id",
            type=openapi.TYPE_NUMBER,
        ),
        'item':openapi.Schema(
            title="The text content",
            type=openapi.TYPE_OBJECT,
            properties= {
                'content_type':openapi.Schema(
                    title="Contennt type",
                    type=openapi.TYPE_STRING,
                ),
                'title':openapi.Schema(
                    title="Text Content title",
                    type=openapi.TYPE_STRING,
                ),
                'content':openapi.Schema(
                    title="text content",
                    type=openapi.TYPE_STRING,
                ),
                "owner": openapi.Schema(
                    title="Owner of this content",
                    type=openapi.TYPE_NUMBER,
                ),
            }
        )
    },
)

image_content_resp = openapi.Schema(
    title=f'Image Content',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            title="Content id",
            type=openapi.TYPE_NUMBER,
        ),
        'order': openapi.Schema(
            title="Content order within parent module",
            type=openapi.TYPE_NUMBER,
        ),
        'module': openapi.Schema(
            title="Perent module id",
            type=openapi.TYPE_NUMBER,
        ),
        'item':openapi.Schema(
            title="The text content",
            type=openapi.TYPE_OBJECT,
            properties= {
                'content_type':openapi.Schema(
                    title="Contennt type",
                    type=openapi.TYPE_STRING,
                ),
                'title':openapi.Schema(
                    title="Text Content title",
                    type=openapi.TYPE_STRING,
                ),
                'file':openapi.Schema(
                    title="file url",
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI
                ),
                "owner": openapi.Schema(
                    title="Owner of this content",
                    type=openapi.TYPE_NUMBER,
                ),
            }
        )
    },
)

file_content_resp = openapi.Schema(
    title=f'File Content',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            title="Content id",
            type=openapi.TYPE_NUMBER,
        ),
        'order': openapi.Schema(
            title="Content order within parent module",
            type=openapi.TYPE_NUMBER,
        ),
        'module': openapi.Schema(
            title="Perent module id",
            type=openapi.TYPE_NUMBER,
        ),
        'item':openapi.Schema(
            title="The file content",
            type=openapi.TYPE_OBJECT,
            properties= {
                'content_type':openapi.Schema(
                    title="Contennt type",
                    type=openapi.TYPE_STRING,
                ),
                'title':openapi.Schema(
                    title="File Content title",
                    type=openapi.TYPE_STRING,
                ),
                'file':openapi.Schema(
                    title="file url",
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI
                ),
                "owner": openapi.Schema(
                    title="Owner of this content",
                    type=openapi.TYPE_NUMBER,
                ),
            }
        )
    },
)

video_content_resp = openapi.Schema(
    title=f'Video Content',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            title="Content id",
            type=openapi.TYPE_NUMBER,
        ),
        'order': openapi.Schema(
            title="Content order within parent module",
            type=openapi.TYPE_NUMBER,
        ),
        'module': openapi.Schema(
            title="Perent module id",
            type=openapi.TYPE_NUMBER,
        ),
        'item':openapi.Schema(
            title="The video content",
            type=openapi.TYPE_OBJECT,
            properties= {
                'content_type':openapi.Schema(
                    title="Contennt type",
                    type=openapi.TYPE_STRING,
                ),
                'title':openapi.Schema(
                    title="video Content title",
                    type=openapi.TYPE_STRING,
                ),
                'url':openapi.Schema(
                    title="vidoe url",
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_URI
                ),
                "owner": openapi.Schema(
                    title="Owner of this content",
                    type=openapi.TYPE_NUMBER,
                ),
            }
        )
    },
)


text_req_body_schema = openapi.Schema(
    title="Text Serializer",
    type=openapi.TYPE_OBJECT,
    properties= {
        'title':openapi.Schema(
            title="Text Content title",
            type=openapi.TYPE_STRING,
        ),
        'content':openapi.Schema(
            title="text content",
            type=openapi.TYPE_STRING,
            
        ),
    },
    required=['content']
)
image_req_body_schema=openapi.Schema(
    title="Image Serializer",
    type=openapi.TYPE_OBJECT,
    properties= {
        'title':openapi.Schema(
            title="Image Content title",
            type=openapi.TYPE_STRING,
        ),
        'file':openapi.Schema(
            title="Image file",
            type=openapi.TYPE_FILE,
            
        ),
    },
    required=['file']
)
file_req_body_schema = openapi.Schema(
    title="Image Serializer",
    type=openapi.TYPE_OBJECT,
    properties= {
        'title':openapi.Schema(
            title="Image Content title",
            type=openapi.TYPE_STRING,
        ),
        'file':openapi.Schema(
            title="file ",
            type=openapi.TYPE_FILE,
            
        ),
    },
    required=['file']
)

video_req_body_schema =  openapi.Schema(
    title="Video Serializer",
    type=openapi.TYPE_OBJECT,
    properties= {
        'title':openapi.Schema(
            title="Video Content title",
            type=openapi.TYPE_STRING,
        ),
        'url':openapi.Schema(
            title="vidoe url",
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI
            
        ),
    },
    required=['url']
)
response = """{
    "id": 34,
    "order": 2,
    "module": 6,
    "item": {
        "content_type": "text",
        "title": "bloop",
        "content": "hccccccccccccccccccccccc",
        "owner": 7
    }
}
"""