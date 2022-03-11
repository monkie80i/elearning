from django.contrib.auth.models import Group
from re import template
from django.shortcuts import render,redirect,get_object_or_404
#from courses.models import Course
from .models import Profile, User
from .forms import UserForm,UserProfileEditForm
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.views import View
import copy,traceback,sys
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from courses.views import PaginateMixin
from django.templatetags.static import static   

# Create your views here.



class UserHomeView(View,LoginRequiredMixin):
    template_name = 'accounts/home.html'
    
    def dispatch(self, request, *args, **kwargs):
        max_courses = 5
        self.user = request.user
        if self.user.is_teacher:
            #courses = Course.objects.filter(user = request.user)[:max_courses]
            self.context_object = {
                'courses':courses,
                'user':self.user
            }
            self.template_name = 'accounts/teacher_home.html'
        if self.user.is_student:
            #courses = Course.objects.filter(students=self.user)[:max_courses]
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
        return render(request,self.template_name,{'form':form,'user_type':user_type})
    
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
                    profile = Profile(user=instance)
                    profile.save()
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


class UserProfilePrivateView(View,LoginRequiredMixin):
    template_name = 'accounts/form.html'
    form_class = UserProfileEditForm
    
    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(User,id=request.user.id)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        form_data = {
            'first_name':self.user.first_name,
            'last_name':self.user.last_name,
            'pic':self.user.profile.pic,
            'dob':self.user.profile.dob,
            'professional_title':self.user.profile.professional_title
        }
        form = self.form_class(initial=form_data)
        context ={
            'user':self.user,
            'form':form
        }
        return render(request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        print("here")
        form = self.form_class(request.POST or None,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            self.user.first_name = cd['first_name']
            self.user.last_name = cd['last_name']
            self.user.profile.dob = cd['dob']
            self.user.profile.pic = cd['pic']
            self.user.profile.professional_title = cd['professional_title']
            self.user.save()
            self.user.profile.save()
        return redirect('user_profile_private')

user_profile_private_view = UserProfilePrivateView.as_view()

class ProfilePublicView(PaginateMixin,View,LoginRequiredMixin):
    template_name = 'accounts/public_profile.html'
    page_size = 5

    def get(self,request,user_id, *args, **kwargs):
        if user_id:
            user_obj = get_object_or_404(User,id=user_id)
        else:
            raise Http404("No User Id in the parameters")
        courses = user_obj.courses.all()
        print(user_obj,courses)
        pagination_url = reverse_lazy('user_profile_public',args=[user_id])
        context_obj = {
            'pagination_url':pagination_url,
            'user_obj':user_obj,
            'default_user_image':static('images/default-user-image.png')
        }
        total_pages = self.get_total_pages(courses)
        courses = self.paginate(courses)
        context_obj['courses'] = courses
        context_obj['page_number'] = self.page_number
        context_obj['total_pages'] = total_pages
        #print(context_obj)
        return render(request,self.template_name,context_obj)

profile_public_view = ProfilePublicView.as_view()