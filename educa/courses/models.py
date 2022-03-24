from distutils.archive_util import make_zipfile
from pyexpat import model
import re
from django.db import models
from adminManager.models import User
from .fields import OrderField
from django.template.loader import render_to_string
# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Course(models.Model):
    user = models.ForeignKey(User,related_name = 'courses',on_delete=models.DO_NOTHING,null=True,blank=True)
    subject = models.ForeignKey(Subject,related_name = 'courses',on_delete=models.DO_NOTHING,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated']
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = OrderField(blank=True,for_field='course')

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.order}.{self.title}'

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Content(models.Model):
    module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE,null=True,blank=True)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,related_name='content',limit_choices_to={'model__in':('text','image','file','video')},null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,blank=True)
    item = GenericForeignKey('content_type','object_id')
    order = OrderField(blank=True,for_field='module')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']



class ItemBase(models.Model):
    owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string(f'content/{self._meta.model_name}.html',{'item':self})

    def serialize(self):
        #return item_serializer[self._meta.model_name](self).data
        pass

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField(null=True,blank=True)

class Image(ItemBase):
    file = models.FileField(upload_to='content_images',null=True,blank=True)

class File(ItemBase):
    file = models.FileField(upload_to='content_files',null=True,blank=True)

class Video(ItemBase):
    url = models.URLField(null=True,blank=True)