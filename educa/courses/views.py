
import collections
from distutils.log import Log
import imp
from mimetypes import init
from multiprocessing import context
from tempfile import template
from tkinter import Image
from typing import Reversible
from django.shortcuts import render,redirect
from django.views import View
from .models import Subject,Course,Module,Content
from django.urls import reverse_lazy
from .forms import CourseForm,ModuleForm,CourseEnrollForm
from django.shortcuts import get_object_or_404
from django.http import Http404,HttpResponse,JsonResponse
#from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView #CreateView, UpdateView,
from django.core.exceptions import ObjectDoesNotExist
import copy,traceback,sys,json,math
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.apps import apps
from django.forms.models import modelform_factory
from django.forms import Form
from django.db.models import Count
from django import forms
from utils.widgets import MyFileInput
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static   

#helpers

def is_add_another(request):
    return 'add' in request.POST.dict()


def paginate(qs,page_size,page_number):
    """Thake s queryset or an list ,
    page_size is the number of item in one page,
    page_number starts from 1 to length of qs/page_size
    """
    start = (page_number-1)*page_size
    end = page_number*page_size
    return qs[start:end]

# Create your views here.

#MIXINS


class SubjectQSMixin(object):
    subjects_qs = Subject.objects.all()
    all_subjects = [subject.title for subject in subjects_qs]

class OwnerMixin(object):
    def setup(self, request,*args, **kwargs):
        self.qs = self.model.objects.filter(user=request.user)
        return super().setup(request, *args, **kwargs)

class PaginateMixin(object):
    """helps in pagination
        requires a url of the same with extra 'page_number' arg.

    """

    page_size = 3
    
    def dispatch(self, request, *args, **kwargs):
        self.page_number = 1
        if 'page_number' in self.kwargs:
            self.page_number = self.kwargs['page_number']
        return super().dispatch(request, *args, **kwargs)
    

    def paginate(self,qs):
        """Thake s queryset or an list ,
        page_size is the number of item in one page,
        page_number starts from 1 to length of qs/page_size
        """
        start = (self.page_number-1)*self.page_size
        end = self.page_number*self.page_size
        return qs[start:end] 

    def get_total_pages(self,qs):
        """gets the total number of pages"""
        return math.ceil(qs.count()/self.page_size)

#Course Views

class OwnerCourseMixin(OwnerMixin,SubjectQSMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    list_template_name = 'manage/courses/list.html'
    edit_template_name = 'manage/courses/form.html'

class ManageCourseView(OwnerCourseMixin,PaginateMixin,View):
    permission_required = 'courses.view_course'
    all_subjects = Subject.objects.all()
    page_size = 5

    def get(self,request,subject=None,*args,**kwargs):
        if subject.lower() not in (None,'all'):
            subject = get_object_or_404(self.all_subjects,slug=subject)
            courses = self.qs.filter(subject__title=subject)
            pagination_url = reverse_lazy('manage_course_list',args=[subject])
        else:   
            courses = self.qs
            subject = None
            pagination_url = reverse_lazy('manage_course_list',args=['all'])

        print(subject)
        context_obj = {
            'subject':subject,
            'all_subjects': self.all_subjects,
            'pagination_url': pagination_url,
        }
        total_pages = self.get_total_pages(courses)
        courses = self.paginate(courses)
        context_obj['object_lsit'] = courses
        context_obj['page_number'] = self.page_number
        context_obj['total_pages'] = total_pages
        print(context_obj)
        return render(request,self.list_template_name,context_obj)

manage_course_view = ManageCourseView.as_view()

class CourseCreateView(OwnerCourseMixin,View):
    permission_required = 'courses.add_course'
    form_class = CourseForm
    
    def get(self,request):
        context_obj = {
            'form':self.form_class()
        }
        return render(request,self.edit_template_name,context_obj)
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                if is_add_another(request):
                    return redirect('course_create')
                return redirect(reverse_lazy('manage_course_detail',args=[instance.id]))
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
    template_name = 'manage/courses/form.html'
    form_class = CourseForm

    def get(self,request,id):
        course_obj = get_object_or_404(self.qs,id=id)
        context_obj = {
            'form':self.form_class(instance=course_obj),
            'object':course_obj
        }
        return render(request,self.edit_template_name,context_obj)
            
    
    def post(self,request,id):
        course_obj = get_object_or_404(self.qs,id=id)
        form = self.form_class(request.POST or None,instance=course_obj)
        if form.is_valid():
            instance = form.save()
            if is_add_another(request):
                return redirect('course_create')
            return redirect(reverse_lazy('manage_course_detail',args=[instance.id]))

course_update_view = CourseUpdateView.as_view()

class CourseDeleteView(OwnerCourseMixin,DeleteView):
    permission_required = 'courses.delete_course'
    success_url = '/manage/course/list/all'
    template_name = 'manage/courses/delete.html'

course_delete_view =CourseDeleteView.as_view()

class CourseDetailView(OwnerCourseMixin,View):
    template_name = 'manage/courses/detail.html'
    permission_required = 'courses.view_course'

    def get(self,request,id):
        course = get_object_or_404(self.qs,id=id)
        modules = course.modules.all()
        context_obj = {
            'course':course,
            'modules':modules
        }
        return render(request,self.template_name,context_obj)

course_detail_view = CourseDetailView.as_view()

#Module Views
class CourseModuleMixin(LoginRequiredMixin):
    model = Module
    fields = ['title', 'description']
    edit_template_name = 'manage/modules/form.html'
    
class ModuleCreateUpdateView(CourseModuleMixin,View):
    form_class = ModuleForm
    modules = None
    module = None
    context = {}

    def setup(self, request,course_id,id=None ,*args, **kwargs):
        self.course = get_object_or_404(Course,id=course_id,user=request.user)
        if id:
            self.modules = self.model.objects.filter(course=self.course)
            self.module = get_object_or_404(self.modules,id=id)
        return super().setup(request,course_id,id=None, *args, **kwargs)

    def get(self,request,course_id,id=None):
        self.context['course_id'] = course_id
        if id:
            form = self.form_class(instance=self.module)
            self.context['object'] = self.module
            self.context['form'] = form
        else:
            form =  self.form_class()
            self.context['form'] = form
        return render(request,self.edit_template_name,self.context)

    def post(self,request,course_id,id=None):
        form = self.form_class(request.POST or None,instance=self.module)
        if form.is_valid():
            if not id :
                instance = form.save(commit=False)
                instance.course = self.course
                instance.save()
            else:
                instance = form.save()
            if is_add_another(request):
                return redirect('create_module',course_id)
        return redirect('module_content_list',instance.id)


module_create_update_view = ModuleCreateUpdateView.as_view()

class ModuleDeleteView(CourseModuleMixin,DeleteView,PermissionRequiredMixin):
    template_name = 'manage/modules/delete.html'
    permission_required = 'module.delete_module'
    #permission_required = 'courses.delete_course'
    def setup(self, request,course_id, *args, **kwargs):
        self.success_url = reverse_lazy('manage_course_detail',args=[course_id])
        return super().setup(request, *args, **kwargs)

module_delete_view =ModuleDeleteView.as_view()


#CONTENT
class ContentCreateUpdateView(View,LoginRequiredMixin):
    Model = None
    module = None
    obj = None
    template_name =  'manage/contents/form.html'

    def get_model(self,model_name):
        if model_name in ('text','image','file','video'):
            return apps.get_model(app_label='courses',model_name=model_name)
        return None
    
    def get_form(self,model,*args,**kwargs):
        widgets = None
        #print(model._meta.model_name)
        if model._meta.model_name in ('file','image'):
            widgets = {
                #'file': forms.FileInput()
                'file':MyFileInput()
            }

        Form =  modelform_factory(
            model=model,
            exclude=['order','owner','created','updated'],
            widgets=widgets
            )  
        base_fields = Form.base_fields
        for fields in base_fields.values():
            fields.widget.attrs['class']='form-control border-primary'
            fields.required = True
        
        return Form(*args,**kwargs)

    def dispatch(self, request,module_id,model_name,id=None, *args, **kwargs):
        self.Model = self.get_model(model_name)
        self.module =get_object_or_404(Module,id=module_id,course__user=request.user)# this will ensure only the owner can edit this modlue
        if id:
            self.obj = get_object_or_404(self.Model,id=id,owner = request.user)
        return super().dispatch(request,module_id,model_name,id, *args, **kwargs)

    def get(self, request,module_id,model_name,id=None):
        form = self.get_form(self.Model,instance=self.obj)
        context_obj = {
            'type': model_name.capitalize(),
            'form':form,
            'object':self.obj,
            'module':self.module
        }
        return render(request,self.template_name,context_obj)

    def post(self, request,module_id,model_name,id=None):
        form = self.get_form(
            self.Model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module = self.module,item=obj)
            if is_add_another(request):
                next_content_type = request.POST.dict()['add']
                if next_content_type not in ('text','image','file','video'):
                    next_content_type = 'text'
                return redirect('create_content',module_id,next_content_type)
            return redirect('module_content_list',module_id)
        return render(request,self.template_name,{'form':form,'object':self.obj})

content_create_update_view = ContentCreateUpdateView.as_view()

class ContentDeleteView(View,LoginRequiredMixin):
    content_obj = None
    template_name = 'manage/contents/delete.html'
    #permission_required = 'module.delete_module'

    def dispatch(self, request,content_id, *args, **kwargs):
        self.content_obj = get_object_or_404(Content,id=content_id,module__course__user=request.user)
        return super().dispatch(request, content_id,*args, **kwargs)

    def get(self,request,content_id, *args, **kwargs):
        form = Form
        context_obj = {
            'form':form,
            'object':self.content_obj,
        }
        return render(request,self.template_name,context_obj)
    
    def post(self,request,content_id, *args, **kwargs):
        module = self.content_obj.module
        print('mod _ id',module.id)
        self.content_obj.item.delete()
        self.content_obj.delete()
        return redirect('module_content_list',module.id)


        
content_delete_view =ContentDeleteView.as_view()

#Manage Content
class ManageModuleContentList(View,LoginRequiredMixin):
    template_name = 'manage/contents/list.html'

    def get(self,request,module_id,*args,**kwargs):
        module = get_object_or_404(Module,id=module_id,course__user=request.user)
        return render(request,self.template_name,{'module':module})


manage_module_content_list = ManageModuleContentList.as_view()

#public views




class CourseListView(PaginateMixin,View):
    template_name = 'courses/list.html'
    page_size = 5

    def get(self,request,subject=None, *args, **kwargs):
        subjects = Subject.objects.annotate(total_courses = Count('courses'))
        courses = Course.objects.all().order_by('-updated').annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject,slug=subject)
            courses = courses.filter(subject=subject)
            pagination_url = reverse_lazy('course_list_subject',args=[subject.slug])
        else:
            pagination_url = reverse_lazy('course_list')
        context_obj = {
            'all_subjects':subjects,
            'subject':subject,
            'pagination_url':pagination_url,
            'default_user_image':static('images/default-user-image.png')
        }
        total_pages = self.get_total_pages(courses)
        courses = self.paginate(courses)
        context_obj['courses'] = courses
        context_obj['page_number'] = self.page_number
        context_obj['total_pages'] = total_pages
        #print(context_obj)
        return render(request,self.template_name,context_obj)

course_list_view = CourseListView.as_view()

class PublicCourseDetailView(View):
    template_name = 'courses/detail.html'

    def get(self,request,id, *args, **kwargs):
        course = get_object_or_404(Course,id=id)
        form = CourseEnrollForm(initial={'course':course})
        context_obj = {
            'course':course,
            'form':form
        }
        return render(request,self.template_name,context_obj)

public_course_detail = PublicCourseDetailView.as_view()

class CourseEnrollView(View,LoginRequiredMixin):
    form_class = CourseEnrollForm

    def get_success_url(self):
        return reverse_lazy('student_course_detail',self.course.id)

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.course = form.cleaned_data['course']
            self.course.students.add(self.request.user)
            return redirect('student_course_detail',self.course.id)

course_enroll_view = CourseEnrollView.as_view()

class StudentCourseDetailView(View,LoginRequiredMixin):
    template_name = 'students/course/detail.html'
    def get(self,request,course_id,*args,**kwargs):
        course = get_object_or_404(Course,id=course_id,students=request.user)
        context = {'course':course}
        if 'module_id' in self.kwargs:
            context['module'] = get_object_or_404(Module,id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all().first()
        return render(request,self.template_name,context)

student_course_detail_view = StudentCourseDetailView.as_view()

class StudentCourseListView(PaginateMixin,View,LoginRequiredMixin):
    template_name = 'students/course/list.html'
    page_size = 5

    def get(self,request,*args,**kwargs):
        courses = Course.objects.filter(students__in=[request.user])
        pagination_url = reverse_lazy('student_course_list')
        context_obj = {
            'pagination_url':pagination_url
        }
        total_pages = self.get_total_pages(courses)
        courses = self.paginate(courses)
        context_obj['courses'] = courses
        context_obj['page_number'] = self.page_number
        context_obj['total_pages'] = total_pages
        #print(context_obj)
        return render(request,self.template_name,context_obj)

student_course_list_view = StudentCourseListView.as_view()


class ManageContentPreView(View,LoginRequiredMixin):
    template_name = 'manage/contents/preview.html'

    def get(self,request,course_id,*args,**kwargs):
        course = get_object_or_404(Course,id=course_id,user=request.user)
        context = {'course':course}
        if 'module_id' in self.kwargs:
            context['module'] = get_object_or_404(Module,id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all().first()
        return render(request,self.template_name,context)

manage_course_preview = ManageContentPreView.as_view()

class CourseUnEnrollView(View,LoginRequiredMixin):
    form_class = CourseEnrollForm
    template_name = 'students/course/confirm_unenroll.html'
    context = {}

    def get_success_url(self):
        return reverse_lazy('student_course_list')

    def get(self,request,course_id,*args,**kwargs):
        course = get_object_or_404(Course,id=course_id,students__in=[request.user])
        form = self.form_class({'course':course})
        self.context['course'] = course
        self.context['form'] = form
        return render(request,self.template_name,self.context)

    def post(self,request,course_id,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.course = form.cleaned_data['course']
            self.course.students.remove(self.request.user)
        return redirect(self.get_success_url())
        

course_un_enroll_view = CourseUnEnrollView.as_view()

#ordering Views


@csrf_exempt
@login_required
def module_order(request,*args, **kwargs):
    output = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            for id,order in data.items():
                print(id,order)
                Module.objects.filter(id=id,course__user = request.user).update(order=order)
            output = {'message':'OK'}
            return JsonResponse(output)
        except Exception as e:
            print(e)
            output['message'] = 'NOT OK'
            return JsonResponse(output)
    output = {'message':'METHOD ERROR'}
    return JsonResponse(output)

@csrf_exempt
@login_required
def content_order(request,*args, **kwargs):
    output = {}
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            for id,order in data.items():
                print(id,order)
                Content.objects.filter(id=id,module__course__user = request.user).update(order=order)
            output = {'message':'OK'}
            return JsonResponse(output)
        except Exception as e:
            print(e)
            output['message'] = 'NOT OK'
    return JsonResponse({'message':'METHOD ERROR'})