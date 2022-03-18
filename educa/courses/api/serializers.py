import imp
from sys import modules
from rest_framework import serializers
from ..models import Subject,Course,Module,Content,Text,Image,File,Video
from adminManager.api.serializers import UserBasicSzr

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'title',
            'slug'
        ]


#for public course list
class ModuleSerializerForCourse(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'order',
        ]
        read_only_fields = fields

class PublicCourseListSerializer(serializers.ModelSerializer):
    user = UserBasicSzr()
    subject = SubjectSerializer()
    class Meta:
        model = Course
        fields = [
            'id',
            'user',
            'subject',
            'title',
            'slug',
            'overview'
        ]
        read_only_fields = fields



class PublicCourseSerializer(serializers.ModelSerializer):
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
        read_only_fields = fields


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'order',
            'course'
        ]
        read_only_fields = ['id','course']


# Private 

