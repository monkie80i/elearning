from django import forms
from .models import Course,Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'subject','title','overview'
        ]
        
