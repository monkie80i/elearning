from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email','is_teacher','is_student']

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    pic = models.FileField(upload_to='profilePics',null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    professional_title = models.CharField(max_length=100,blank=True,null=True)
    visible_on_profile =  models.CharField(max_length=100,blank=True,null=True)

    def visible_on_profile_add(self):
        pass

    def visible_on_profile_remove(self):
        pass

    def is_visible_on_profile(self):
        pass

    def visible_on_profile_fields(self):
        pass