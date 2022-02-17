from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.title


