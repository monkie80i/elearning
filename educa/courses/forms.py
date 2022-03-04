from django import forms
from .models import Course,Module

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'subject','title','overview'
        ]
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border-primary'
        
class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            'title','description'
        ]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border-primary'
        #self.set_required()

class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control border-primary'


    
