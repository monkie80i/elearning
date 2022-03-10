from dataclasses import field
from pyexpat import model
from tkinter import Widget
from tokenize import blank_re
from .models import User,Profile
from django import forms
from utils.widgets import MyFileInput

class UserForm(forms.ModelForm):
    password_1 = forms.CharField(max_length=100,label='Enter Passowrd',required=True,widget=forms.PasswordInput)
    password_2 = forms.CharField(max_length=100,label='Re-enter Passwrod',required=True,widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'is_student',
            'is_teacher'
        ]
        widgets = {
            'is_student': forms.HiddenInput(),
            'is_teacher': forms.HiddenInput(),

        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border-primary'


class UserProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    pic = forms.FileField(widget=MyFileInput())
    dob = forms.DateField()
    professional_title = forms.CharField(max_length=100)

    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border-primary'
    
    def save(self,user_object):
        try:
            cd = self.cleaned_data
            user_model_fields = ['first_name','last_name']
            profile_model_fields = ['dob','professional_title']
            for key in cd.keys():
                print(key,cd[key])
                if key in user_model_fields:
                    user_object.key = cd[key]
                elif key in profile_model_fields:
                    user_object.profile.key = cd[key]
            user_object.save()
            user_object.profile.save()
        except Exception as e:
            print(e)
