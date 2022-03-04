from importlib.resources import contents
from re import sub
from turtle import title
from urllib import response
from django.test import RequestFactory, TestCase,Client,LiveServerTestCase
from .models import Subject, User
from django.urls import reverse,reverse_lazy
from django.conf import settings
from .models import Course,Module,Content,Text
from django.contrib.auth.models import Group,Permission
# Create your tests here.
t_perm_codes = [
    'add_contenttype', 'change_contenttype', 'delete_contenttype', 'view_contenttype', 
    'add_content', 'change_content', 'delete_content', 'view_content', 'add_course', 
    'change_course', 'delete_course', 'view_course', 'add_file', 'change_file', 
    'delete_file', 'view_file', 'add_image', 'change_image', 'delete_image', 
    'view_image', 'add_module', 'change_module', 'delete_module', 'view_module', 
    'add_subject', 'change_subject', 'delete_subject', 'view_subject', 'add_text', 
    'change_text', 'delete_text', 'view_text', 'add_video', 'change_video', 'delete_video',
    'view_video'
]
t_perms = [ Permission.objects.get(codename=p) for p in t_perm_codes]

s_perm_codes =[
    'change_profile', 'view_profile', 'change_user', 'view_user',
    'view_contenttype', 'view_content', 'view_course', 'view_file', 
    'view_image', 'view_module', 'view_subject', 'view_text', 'view_video'
]

s_perms = [ Permission.objects.get(codename=p) for p in s_perm_codes]



class ModuleOrderTestCase(TestCase):
    def setUp(self):
        self.c1 = Course.objects.create(title='Course 1')
        self.m11 = Module.objects.create(title='Module 1.1',course = self.c1 )
        self.m12 = Module.objects.create(title='Module 1.2',course = self.c1 )
        self.m13 = Module.objects.create(title='Module 1.3',course = self.c1 )
        
    def test_module_order(self):
        print(self.m11.order,self.m12.order,self.m13.order)
    
class CourseViewsTestCase(TestCase):
    def setUp(self):
        self.password = 'teacher1234'
        self.username='teacher1'
        self.username2 ='student1'
        self.password2 = 'student1234'
        self.t1_data = {
            'username':self.username,
            'password_1':self.password,
            'password_2':self.password,
            'email':'ashdksj@gmail.com',
            'is_student':False,
            'is_teacher':True
        }
        self.s1_data =  {
            'username':self.username2,
            'password_1':self.password2,
            'password_2':self.password2,
            'email':'ashdksj@gmail.com',
            'is_student':True,
            'is_teacher':False
        }
        t_g = Group.objects.create(name='teacher')
        
        s_g = Group.objects.create(name='student')
        t_perms = [ Permission.objects.get(codename=p) for p in t_perm_codes]
        t_g.permissions.set(t_perms)
        s_g.permissions.set(s_perms)
        t_g.save()
        s_g.save()
        #print(type(teacher_group))
        # groups doesnot exist et o need to add groups and permissions

        self.t_client = Client()
        self.t_client.post(reverse_lazy('user_registration',args=['teacher']),data=self.t1_data)
        self.s_client = Client()
        self.s_client.post(reverse_lazy('user_registration',args=['student']),data=self.s1_data)
        self.t_client.login(username=self.username,password=self.password)
        self.s_client.login(username=self.username2,password=self.password2)

    def test_get_create_form(self):
        response = self.t_client.get(reverse_lazy('course_create'))
        self.assertEqual(response.status_code,200)
        data = {
            'subject':'1',
            'title':'ddddd',
            'overview':'dfsdfskdfhsdf'
        }
        response = self.t_client.post(reverse_lazy('course_create'),data)
        c = Course.objects.latest('created')
        self.assertEqual(c.title,data['title'])
        self.assertEqual(response.status_code,302)
    
    def test_manage_course_list(self):
        response = self.t_client.get(reverse_lazy('manage_course_list',args=['all']))
        self.assertEqual(response.status_code,200)
        response = self.s_client.get(reverse_lazy('manage_course_list',args=['all']))
        self.assertEqual(response.status_code,200)
    


class ModuleCreateUpdateTestCase(TestCase):
    def setUp(self):
        self.password = 'teacher1234'
        self.username='teacher1'
        self.username2 ='student1'
        self.password2 = 'student1234'
        self.t1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='ashdksj@gmail.com',
            is_student=False,
            is_teacher=True
        )
        
        self.clent = Client()
        self.clent.login(username=self.username,password=self.password)

        subjects = ['science','maths']
        self.subject_objects = {}
        for sub in subjects:
            self.subject_objects[sub] = Subject.objects.create(title=sub)
        #print('subjects:',self.subject_objects)

        self.course1 = Course.objects.create(user=self.t1,subject = self.subject_objects['science'],title='Course 1')


    def test_module_creat_update(self):
        data = {
            'title':'My Title',
            'description':'This is desc'
        }

        response = self.clent.post(reverse_lazy('create_module',args=[self.course1.id]),data)
        self.assertEqual(response.status_code,302)
        all_module= Module.objects.all()
        print('all modules:',all_module[0].course)
        self.assertEqual(Module.objects.all().exists(),True)

        self.assertEqual(Module.objects.filter(course__id=self.course1.id).exists(),True)
    
    def test_module_update(self):
        m1 = Module.objects.create(course=self.course1,title='Olc Module')
        new_data = {
            'title':'My New Title',
            'description':'This is New desc'
        }
        self.assertEqual(Module.objects.filter(course__id=self.course1.id).first().title,'Olc Module')
        response = self.clent.post(reverse_lazy('update_module',args=[self.course1.id,m1.id]),new_data)
        print('url',response.url)
        self.assertEqual(Module.objects.filter(course__id=self.course1.id).first().title,'My New Title')


    def test_module_delete(self):
        m1 = Module.objects.create(course=self.course1,title='Olc Module')
        pass

    def test_create_and_add_another(self):
        data = {
            'title':'My Title',
            'description':'This is desc',
            'add':'dfsfd'
        }

        response = self.clent.post(reverse_lazy('create_module',args=[self.course1.id]),data)
        self.assertEqual(response.url,'/course/1/module/create/')
        all_module= Module.objects.all()
        print('all modules:',all_module[0].course)
        self.assertEqual(Module.objects.all().exists(),True)
        self.assertEqual(Module.objects.filter(course__id=self.course1.id).exists(),True)
    
    def test_update_and_add_another(self):
        m1 = Module.objects.create(course=self.course1,title='Olc Module')
        new_data = {
            'title':'My New Title',
            'description':'This is New desc',
            'add':'dfsfd'
        }
        self.assertEqual(Module.objects.filter(course__id=self.course1.id).first().title,'Olc Module')
        response = self.clent.post(reverse_lazy('update_module',args=[self.course1.id,m1.id]),new_data)
        self.assertEqual(response.url,f'/course/{self.course1.id}/module/create/')
        self.assertEqual(Module.objects.filter(course__id=self.course1.id).first().title,'My New Title')
        
class InstructorPermissionTestCase(TestCase):
    def setUp(self):
        self.password = 'teacher1234'
        self.username='teacher1'
        self.username2 ='student1'
        self.password2 = 'student1234'
        self.t1_data = {
            'username':self.username,
            'password_1':self.password,
            'password_2':self.password,
            'email':'ashdksj@gmail.com',
            'is_student':False,
            'is_teacher':True
        }
        self.s1_data =  {
            'username':self.username2,
            'password_1':self.password2,
            'password_2':self.password2,
            'email':'ashdksj@gmail.com',
            'is_student':True,
            'is_teacher':False
        }


        
    def test_group_added_on_registration(self):
        t_client = Client()
        response = t_client.post(reverse_lazy('user_registration',args=['teacher']),data=self.t1_data)
        #self.assertEqual(response.url,reverse_lazy('user_home'))
        self.assertEqual(response.status_code,200)
        user = User.objects.first()
        self.assertEqual(user.groups.first().name,'teacher')
        s_client = Client()
        response = s_client.post(reverse_lazy('user_registration',args=['student']),data=self.s1_data)

class ContentCreateUpdateTestCase(TestCase):
    def setUp(self):
        self.password = 'teacher1234'
        self.username='teacher1'
        self.username2 ='student1'
        self.password2 = 'student1234'
        self.t1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='ashdksj@gmail.com',
            is_student=False,
            is_teacher=True
        )

        self.s1 = User.objects.create_user(
            username=self.username2,
            password=self.password2,
            email='ashdksj@gmail.com',
            is_student=True,
            is_teacher=False
        )

        self.co1 = Course.objects.create(user=self.t1,title='Course1')
        self.mo1 =  Module.objects.create(course=self.co1,title='Module1')
        
        self.tclent = Client()
        self.tclent.login(username=self.username,password=self.password)
        #self.sclent = Client()
        #self.sclent.login(username=self.username2,password=self.password2)

    def test_owner_creation_updation_delete(self):
        
        
        response = self.tclent.get(reverse_lazy('create_content',args=[self.mo1.id,'text']))
        
        self.assertEqual(response.status_code,200)
        data =  {
            'title':"New Old Content",
            'content':"This is Old content"
        }
        print(Content.objects.all(),Text.objects.all())
        response = self.tclent.post(reverse_lazy('create_content',args=[self.mo1.id,'text']),data=data)
        self.assertEqual(response.status_code,302)

        print('gensis',Content.objects.all(),Text.objects.all())
        #print(response.url)
        text = Content.objects.filter(module=self.mo1).first()
        self.assertEqual(text.item.owner,self.t1)
        item=text.item
        #print(item.owner,item.title,item.content)
        self.assertEqual(text.item.title,data['title'])
        response = self.tclent.get(reverse_lazy('update_content',args=[self.mo1.id,'text',item.id]))
        self.assertEqual(response.status_code,200)

        new_data =  {
            'title':"New Text Content",
            'content':"This is new content"
        }
        response = self.tclent.post(reverse_lazy('update_content',args=[self.mo1.id,'text',item.id]),data=new_data)
        self.assertEqual(response.status_code,302)

        content = Content.objects.filter(module=self.mo1).first()
        nitem = content.item
        self.assertEqual(nitem.owner,self.t1)
        self.assertEqual(nitem.title,new_data['title'])
        print('after update',Content.objects.all(),Text.objects.all())
        #delteion
        #print('cid:',content.id)
        response = self.tclent.get(reverse_lazy('delete_content',args=[content.id]))
        self.assertEqual(response.status_code,200)
        #print(response.content)
        response = self.tclent.post(reverse_lazy('delete_content',args=[content.id]))
        self.assertEqual(response.status_code,302)
        self.assertEqual(Content.objects.filter(id=content.id).exists(),False)
        print('After Delete',Content.objects.all(),Text.objects.all())
        
    def test_non_owner_creation_updation(self):
        pass

    def test_student_creation_updation(self):
        pass

