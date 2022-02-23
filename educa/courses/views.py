from http.client import HTTPResponse
import imp
from mimetypes import init
from tempfile import template
from django.shortcuts import render,redirect
from django.views import View
from .models import Subject,Course,Module,Content
from django.urls import reverse
from .forms import CourseForm,ModuleForm
from django.shortcuts import get_object_or_404
from django.http import Http404
#from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView #CreateView, UpdateView,
from django.core.exceptions import ObjectDoesNotExist
import copy,traceback,sys,json
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
class SubjectQSMixin(object):
    subjects_qs = Subject.objects.all()
    all_subjects = [subject.title for subject in subjects_qs]

class OwnerMixin(object):
    def setup(self, request,*args, **kwargs):
        self.qs = self.model.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)



#Course Views

class OwnerCourseMixin(OwnerMixin,SubjectQSMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    list_template_name = 'courses/list.html'
    edit_template_name = 'courses/form.html'

class ManageCourseView(OwnerCourseMixin,View):
    permission_required = 'courses.view_course'

    def get(self,request,subject=None):
        if subject not in (None,'all','All'):
            qs = self.qs.filter(subject__title=subject)
        else:   
            qs=self.qs
        return render(request,self.list_template_name,{'object_lsit':qs,'subject':subject,'all_subjects': self.all_subjects})

manage_course_view = ManageCourseView.as_view()

class CourseCreateView(OwnerCourseMixin,View):
    permission_required = 'courses.add_course'
    form_class = CourseForm
    
    def get(self,request):
        context_obj = {
            'form':self.form_class
        }
        return render(request,self.edit_template_name,context_obj)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect(reverse('course_list',args=['all']))
            except Exception as e:
                traceback.print_exc(file=sys.stdout)
                print('e:',e)
        errors = form.errors
        context_obj = {
            'form':self.form_class,
            'errors':errors
        }
        return render(request,self.edit_template_name,context_obj)

course_create_view = CourseCreateView.as_view()

class CourseUpdateView(OwnerCourseMixin,View):
    permission_required = 'courses.change_course'
    template_name = 'courses/form.html'
    form_class = CourseForm

    def get(self,request,id):
        try:
            course_obj = self.qs.filter(id=id).first()
            context_obj = {
                'form':self.form_class(instance=course_obj),
                'object':course_obj
            }
            return render(request,self.edit_template_name,context_obj)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')
            
    
    def post(self,request,id):
        try:
            course_obj = self.qs.filter(id=id).first()
            form = self.form_class(request.POST or None,instance=course_obj)
            if form.is_valid():
                form.save()
                return redirect(reverse('course_list',args=['all']))
                #change to detail
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')


course_update_view = CourseUpdateView.as_view()

class CourseDeleteView(OwnerCourseMixin,DeleteView):
    permission_required = 'courses.delete_course'
    success_url = '/courses/course/list/all/'
    template_name = 'courses/delete.html'
    #permission_required = 'courses.delete_course'

course_delete_view =CourseDeleteView.as_view()

class CourseDetailView(OwnerCourseMixin,View):
    template_name = 'courses/detail.html'
    permission_required = 'courses.view_course'

    def get(self,request,id):
        try:
            course = self.qs.filter(id=id).first()
            modules = course.modules.all()
            context_obj = {
                'course':course,
                'modules':modules
            }
            return render(request,self.template_name,context_obj)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')

course_detail_view = CourseDetailView.as_view()

#Module Views
class CourseModuleMixin(LoginRequiredMixin):
    model = Module
    fields = ['title', 'description']
    edit_template_name = 'modules/form.html'
    
class ModuleCreateUpdateView(CourseModuleMixin,View):
    form_class = ModuleForm

    def setup(self, request,course_id,id=None ,*args, **kwargs):
        self.course = Course.objects.filter(user=request.user).filter(id=course_id).first()
        if not self.course:
            raise Exception('Course Doesnot Exist')
        if id:
            self.modules = self.model.objects.filter(course=self.course)
            self.module = self.modules.filter(id=id).first()
            if not self.module:
                raise Exception('Module Does Not Exist')
        return super().setup(request,course_id,id=None, *args, **kwargs)

    def get(self,request,course_id,id=None):
        try: 
            if id:
                form = self.form_class(instance=self.module)
            else:
                form =  self.form_class()
            return render(request,self.edit_template_name,{'form':form})
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')

    def post(self,request,course_id,id=None):
        try:
            if id:
                form = self.form_class(request.POST or None,instance=self.module)
            else:
                form =  self.form_class()
            data=request.POST.dict()
            is_add_another = 'add' in data.keys()
            print('data:',data)
            if form.is_valid():
                if not id :
                    instance = form.save(commit=False)
                    instance.course = self.course
                    instance.save()
                else:
                    form.save()
                if is_add_another:
                    forms = self.form_class()
                    return render(request,self.edit_template_name,{'form':form})
            return redirect(reverse('course_detail',args=[course_id]))
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')

module_create_update_view = ModuleCreateUpdateView.as_view()

class ModuleDeleteView(CourseModuleMixin,DeleteView,PermissionRequiredMixin):
    template_name = 'modules/delete.html'
    permission_required = 'module.delete_module'
    #permission_required = 'courses.delete_course'
    def setup(self, request,course_id, *args, **kwargs):
        self.success_url = reverse('course_detail',args=[course_id])
        return super().setup(request, *args, **kwargs)

module_delete_view =ModuleDeleteView.as_view()
