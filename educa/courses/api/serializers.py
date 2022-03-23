from dataclasses import field
from importlib.metadata import requires
from pyexpat import model

from wsgiref import validate
from rest_framework import serializers
from ..models import Subject,Course,Module,Content,Text,Image,File,Video
from adminManager.api.serializers import UserBasicSzr
from adminManager.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            'id',
            'title',
            'slug'
        ]

class SubjectReadSerializer(SubjectSerializer):
    class Meta(SubjectSerializer.Meta):
        read_only_fields = [
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




# Private 
class ManageCourseMinSzr(serializers.ModelSerializer):
    subject = SubjectSerializer(many=False)
    modules_count = serializers.IntegerField(source='modules.count')
    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'overview',
            'modules_count'
        ]
        read_only_fields = fields


class CourseSerializer(serializers.ModelSerializer):
    user = UserBasicSzr(many=False,required=False,read_only=True)
    subject = SubjectReadSerializer(many=False,required=False,read_only=True)
    modules = ModuleSerializerForCourse(many=True,required=False,read_only=True)
    modules_count = serializers.IntegerField(source='modules.count',required=False,read_only=True)
    subject_slug = serializers.SlugField(write_only=True,required=True)
    class Meta:
        model = Course
        fields = [
            'id',
            'user',
            'subject',
            'subject_slug',
            'title',
            'overview',
            'modules',
            'modules_count'
        ]
        extra_kwargs = {
            'title': {'required': True},
            'overview': {'required': True},
        }
        read_only_fields = [
            'user',
            'subject',
            'modules',
            'modules_count'
        ]

    def validate_subject_slug(self,value):
        #print("Enter")
        try:
            subject = Subject.objects.get(slug=value)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Invalid Subject slug')
        return subject

    def create(self,validated_data):
        #validated_data is a dictionary
        try:
            subject = validated_data.pop('subject_slug')
        except Exception as e:
            raise ValidationError({'detail':f'{type(e)}{e}'})
        validated_data['subject'] = subject
        return Course.objects.create(**validated_data)
    
    def update(self,instance, validated_data,*args, **kwargs):
        if 'partial' in kwargs:
            print("Is partial Update")
        subject = validated_data.get('subject_slug')
        validated_data['subject'] = subject
        instance.title = validated_data.get('title',instance.title)
        instance.overview = validated_data.get('overview',instance.overview)
        instance.subject = validated_data.get('subject',instance.subject)
        instance.save()
        return instance

class CourseSzeForModule(serializers.ModelSerializer):
    subject = serializers.SlugField(source = "subject.slug")
    modules_count = serializers.IntegerField(source='modules.count')
    class Meta:
        model = Course
        fields = [
            'id',
            'subject',
            'title',
            'overview',
            'modules_count'
        ]
        read_only_fields = fields

class ModuleSerializer(serializers.ModelSerializer):
    content_count = serializers.IntegerField(source='contents.count',read_only=True)
    class Meta:
        model = Module
        fields = [
            'id',
            'title',
            'description',
            'order',
            'contents',
            'content_count',
            'course'
        ]
        """extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
        }"""
        read_only_fields = ['id','course','contents']
    
    def update(self,instance, validated_data,*args, **kwargs):
        #if 'partial' in kwargs:
        #   print("Is partial Update")
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance
    
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        exclude = ['created','updated']

class ItemSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source="_meta.model_name",read_only=True)
    class Meta:
        exclude = ['created','updated']

class TextSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = Text
        extra_kwargs = {
            'content': {'required': True},
        }


class ImageSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = Image
        extra_kwargs = {
            'file': {'required': True},
        }

class FileSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = File
        extra_kwargs = {
            'file': {'required': True},
        }

class VideoSerializer(ItemSerializer):
    class Meta(ItemSerializer.Meta):
        model = Video
        extra_kwargs = {
            'url': {'required': True},
        }
