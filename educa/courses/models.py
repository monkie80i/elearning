from ast import Mod
import imp
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField

#easy import
#from courses.models import Subject,Course,Module

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created',on_delete=models.CASCADE,null=True,blank=True)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True)
    overview = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title
    
class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    order = OrderField(blank=True,for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}.{self.title}'

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE,null=True,blank=True)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model__in':('text','video','image','file')
        },
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(for_fields=['module'],blank=True)

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=250,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()

