from rest_framework import serializers
from .serializers import *
from drf_yasg import openapi
# these are only for schema generation in documentation



class CourseWriteSerializer(serializers.ModelSerializer):
    subject_slug = serializers.SlugField(write_only=True,required=True)
    class Meta:
        model = Course
        fields = [
            'subject_slug',
            'title',
            'overview',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'overview': {'required': True},
        }

class CourseReadSerializer(serializers.ModelSerializer):
    user = UserBasicSzr(many=False)
    subject = SubjectSerializer(many=False)
    modules = ModuleSerializerForCourse(many=True)
    modules_count = serializers.IntegerField(source='modules.count')
    class Meta:
        model = Course
        fields = [
            'id',
            'user',
            'subject',
            'title',
            'overview',
            'modules',
            'modules_count'
        ]