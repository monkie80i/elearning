
from distutils.log import Log
import imp
from mimetypes import init
from multiprocessing import context
from tempfile import template
from typing import Reversible
from django.shortcuts import render,redirect
from django.views import View
from .models import Subject,Course,Module,Content
from django.urls import reverse_lazy
from .forms import CourseForm,ModuleForm,CourseEnrollForm
from django.shortcuts import get_object_or_404
from django.http import Http404,HttpResponse
#from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView #CreateView, UpdateView,
from django.core.exceptions import ObjectDoesNotExist
import copy,traceback,sys,json
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.apps import apps
from django.forms.models import modelform_factory
from django.forms import Form
from django.db.models import Count

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
    list_template_name = 'manage/courses/list.html'
    edit_template_name = 'manage/courses/form.html'

class ManageCourseView(OwnerCourseMixin,View):
    permission_required = 'courses.view_course'
    all_subjects = Subject.objects.all()
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
                return redirect(reverse_lazy('manage_course_list',args=['all']))
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
                return redirect(reverse_lazy('manage_course_list',args=['all']))
                #change to detail
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')


course_update_view = CourseUpdateView.as_view()

class CourseDeleteView(OwnerCourseMixin,DeleteView):
    permission_required = 'courses.delete_course'
    success_url = '/manage/course/list/all'
    template_name = 'manage/courses/delete.html'
    #permission_required = 'courses.delete_course'

course_delete_view =CourseDeleteView.as_view()

class CourseDetailView(OwnerCourseMixin,View):
    template_name = 'manage/courses/detail.html'
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
    edit_template_name = 'manage/modules/form.html'
    
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
                context = {
                    'object':self.module,
                    'form':form,
                    'course_id':course_id
                }
            else:
                form =  self.form_class()
                context = {
                    'form':form,
                    'course_id':course_id
                }
            return render(request,self.edit_template_name,context)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')

    def post(self,request,course_id,id=None):
        try:
            try:
                is_add_another = request.POST.dict().pop('add')
            except:
                is_add_another=False
            if id:
                form = self.form_class(request.POST or None,instance=self.module)
            else:
                form =  self.form_class(request.POST)
            if form.is_valid():
                if not id :
                    instance = form.save(commit=False)
                    instance.course = self.course
                    instance.save()
                else:
                    instance = form.save()
                if is_add_another:
                    return redirect('create_module',course_id)
            return redirect('module_content_list',instance.id)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print('e:',e)
            raise Http404('oops')

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
        Form =  modelform_factory(model=model,exclude=['order','owner','created','updated'])   
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
        print('id',id)

        #print('files',request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module = self.module,item=obj)
            #redirect to content list later 'module_content_list'
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
class CourseListView(View):
    template_name = 'courses/list.html'
    
    def get(self,request,subject=None, *args, **kwargs):
        subjects = Subject.objects.annotate(total_courses = Count('courses'))
        courses = Course.objects.annotate(total_modules=Count('modules'))
        if subject:
            subject = get_object_or_404(Subject,slug=subject)
            courses = courses.filter(subject=subject)
        context_obj = {
            'courses':courses,
            'all_subjects':subjects,
            'subject':subject
        }
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

class StudentCourseListView(View,LoginRequiredMixin):
    template_name = 'students/course/list.html'

    def get(self,request):
        courses = Course.objects.filter(students__in=[request.user])
        return render(request,self.template_name,{'courses':courses})

student_course_list_view = StudentCourseListView.as_view()
