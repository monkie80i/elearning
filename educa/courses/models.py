from distutils.archive_util import make_zipfile
from django.db import models
from adminManager.models import User

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
    subject = models.OneToOneField(Subject,on_delete=models.DO_NOTHING,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    slug = models.SlugField(max_length=200,unique=True,null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.title