import imp
from sys import modules
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
    user = UserBasicSzr(many=False,read_only=True)
    subject = SubjectSerializer(many=False,read_only=True)
    modules = ModuleSerializerForCourse(many=True,read_only=True)
    modules_count = serializers.IntegerField(source='modules.count',read_only=True)
    subject_slug = serializers.SlugField(write_only=True,required=False)
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