from dataclasses import field
from pyexpat import model
from tkinter import Widget
from .models import User,Profile
from django import forms

class UserForm(forms.ModelForm):
    password_1 = forms.CharField(max_length=100,label='Enter Passowrd',required=True)
    password_2 = forms.CharField(max_length=100,label='Re-enter Passwrod',required=True)

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


