from django.contrib.auth.models import Group
from re import template
from django.shortcuts import render,redirect

from courses.models import Course
from .models import User
from .forms import UserForm
from django.http import HttpResponseRedirect,HttpResponse
from django.views import View
import copy,traceback,sys
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.



class UserHomeView(View,LoginRequiredMixin):
    template_name = 'accounts/home.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if self.user.is_teacher:
            courses = Course.objects.filter(user = request.user)
            self.courses = courses[:10] if len(courses)>10 else courses
            self.context_object = {
                'courses':self.courses,
                'user':self.user
            }
            self.template_name = 'accounts/teacher_home.html'
        if self.user.is_student:
            courses = Course.objects.filter(students=self.user)[:10]
            self.context_object = {
                'courses':courses,
                'user':self.user
            }
            self.template_name = 'accounts/student_home.html'
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,self.context_object)

user_home_view = UserHomeView.as_view()

class UserRegistrationView(View):
    template_name = 'registration/register.html'
    form_class = UserForm
    teacher_initail = {'is_teacher':True,'is_student':False}
    student_initail = {'is_teacher':False,'is_student':True}

    def get_inital_of_user_type(self,user_type):
        if user_type in (None,'teacher'):
            initial = self.teacher_initail
        if user_type == 'student':
            initial = self.student_initail
        return initial
    

    def get(self,request,user_type=None,*args,**kwargs):
        initial = self.get_inital_of_user_type(user_type)
        form = self.form_class(initial=initial)
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,user_type=None,*args,**kwargs):
        error = None
        form = self.form_class(request.POST)
        if form.is_valid():
            #print('cleaned data:',form.cleaned_data)
            try:
                cd = form.cleaned_data
                if cd["password_1"] == cd["password_2"]:
                    instance = form.save(commit=False)
                    password = copy.deepcopy(cd["password_1"])
                    instance.set_password(password)
                    instance.save()
                    group = Group.objects.get(name=user_type)
                    group.user_set.add(instance)
                    #print(instance.username,password)
                    user = authenticate(request, username=instance.username, password=password)
                    #print('user',user)
                    if user:
                        login(request,user)
                        #print('rev:',reverse_lazy('teacher_home'))
                        return HttpResponseRedirect(reverse('user_home'))
                else:
                    error = {'message':'password does not match'}
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print('e:',e)

        else:
            error = copy.deepcopy(form.errors.as_data())
        initial = self.get_inital_of_user_type(user_type)
        form = self.form_class(initial=initial)
        return render(request,self.template_name,{'form':self.form_class,'error':error})

user_registration_view = UserRegistrationView.as_view()
