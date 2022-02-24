from django import forms
from .models import Course,Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'subject','title','overview'
        ]
        
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            'title','description'
        ]

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)