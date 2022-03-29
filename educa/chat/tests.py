from django.test import TestCase

from django.test import TestCase,Client
from adminManager.models import  User
from django.urls import reverse,reverse_lazy
from django.conf import settings
from courses.models import Subject,Course,Module,Content,Text
from django.contrib.auth.models import Group,Permission
# data
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

# Create your tests here.
class ChatTestCase(TestCase):
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
        self.co1.students.add(self.s1)
        self.tclent = Client()
        
    
    def test_view(self):
        #anonymous
        response = self.tclent.get(reverse_lazy('chat:course_chat_room',args=[self.co1.id]))
        self.assertEqual(response.status_code,302)
        #teacher
        self.tclent.login(username=self.username,password=self.password)
        response = self.tclent.get(reverse_lazy('chat:course_chat_room',args=[self.co1.id]))
        self.assertEqual(response.status_code,200)
        self.tclent.logout()
        #student
        self.tclent.login(username=self.username2,password=self.password2)
        response = self.tclent.get(reverse_lazy('chat:course_chat_room',args=[self.co1.id]))
        self.assertEqual(response.status_code,200)
        self.tclent.logout()
        
        