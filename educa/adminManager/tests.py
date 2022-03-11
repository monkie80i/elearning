from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase,Client
from .views import user_registration_view as uv
from .models import User,Profile
from django.urls import reverse,reverse_lazy
from django.conf import settings
from django.contrib.auth.models import Group,Permission

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
class RegistrationViewTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = Client()
        self.url = reverse_lazy('user_registration',kwargs={'user_type':'teacher'})
    
    def test_password_doesnot_match(self):
        data = {
            'first_name':'shahzan',
            'last_name':'sadick',
            'username':'sh1',
            'email':'sh1@gmail.com',
            'is_student':False,
            'is_teacher':True,
            'password_1':'abcdef',
            'password_2':'abcde',
        }
        #print(self.url,data)
        response = self.factory.post(self.url,data)
        #print(response.status_code)
        self.assertEqual(User.objects.filter(email=data['email']).exists(),False)
    
    def test_minimum_required_fields(self):
        data = {
            #'first_name':'shahzan',
            #'last_name':'sadick',
            'username':'sh1',
            'email':'sh1@gmail.com',
            'is_student':False,
            'is_teacher':True,
            'password_1':'abcdef',
            'password_2':'abcdef',
        }

        response = self.factory.post(self.url,data)
        self.assertRedirects(response,reverse('user_home'))
        self.assertEqual(User.objects.filter(email=data['email']).exists(),True)

    def test_home_redirection(self):
        data = {
            #'first_name':'shahzan',
            #'last_name':'sadick',
            'username':'sh1',
            'email':'sh1@gmail.com',
            'is_student':False,
            'is_teacher':True,
            'password_1':'abcdef',
            'password_2':'abcdef',
        }

        response = self.factory.post(self.url,data)
        #print(response.content)
        self.assertRedirects(response,reverse('user_home'))
        print(response.headers)
        self.assertEqual(User.objects.filter(email=data['email']).exists(),True)

    def test_login_teacher(self):
        username = 'shahzan1'
        password = 'abcd12345'
        home_url = reverse('user_home')
        login_url = reverse('login')
        user = User.objects.create_user(
            username=username,
            password=password,
            email='ashdksj@gmail.com',
            is_student=False,
            is_teacher=True
        )

        data = {
            'username': username,
            'password':password,
            'next': home_url
        }

        response = self.factory.post(login_url,data)
        self.assertRedirects(response,home_url)
    
    def test_login_student(self):
        username = 'shahzan1'
        password = 'abcd12345'
        home_url = reverse('user_home')
        login_url = reverse('login')
        user = User.objects.create_user(
            username=username,
            password=password,
            email='ashdksj@gmail.com',
            is_student=True,
            is_teacher=False
        )

        data = {
            'username': username,
            'password':password,
            'next': home_url
        }

        response = self.factory.post(login_url,data)
        self.assertRedirects(response,home_url)

    def test_logout(self):
        username = 'shahzan1'
        password = 'abcd12345'
        home_url = reverse('user_home')
        login_url = reverse('login')
        user = User.objects.create_user(
            username=username,
            password=password,
            email='ashdksj@gmail.com',
            is_student=True,
            is_teacher=False
        )

        self.factory.login(username=username,password=password)
        response = self.factory.get(reverse('logout'))
        #self.assertRedirects(response,)

class ProfileCreationOnRegistration(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        t_g = Group.objects.create(name='teacher')
        
        s_g = Group.objects.create(name='student')
        t_perms = [ Permission.objects.get(codename=p) for p in t_perm_codes]
        t_g.permissions.set(t_perms)
        s_g.permissions.set(s_perms)
        t_g.save()
        s_g.save()
        self.factory = Client()
        self.url = reverse_lazy('user_registration',kwargs={'user_type':'teacher'})
    
    def test_profile_creation_teacher_reg(self):
        data = {
            #'first_name':'shahzan',
            #'last_name':'sadick',
            'username':'sh1',
            'email':'sh1@gmail.com',
            'is_student':False,
            'is_teacher':True,
            'password_1':'abcdef',
            'password_2':'abcdef',
        }

        response = self.factory.post(self.url,data)
        print(response.content)
        #self.assertRedirects(response,reverse('user_home'))
        profile= Profile.objects.first()
        user = User.objects.get(username='sh1')
        self.assertEqual(user.profile,profile)

    def test_profile_creation_student_reg(self):
        data = {
            #'first_name':'shahzan',
            #'last_name':'sadick',
            'username':'sh1',
            'email':'sh1@gmail.com',
            'is_student':True,
            'is_teacher':False,
            'password_1':'abcdef',
            'password_2':'abcdef',
        }

        response = self.factory.post(self.url,data)
        print(response.content)
        #self.assertRedirects(response,reverse('user_home'))
        profile= Profile.objects.first()
        user = User.objects.get(username='sh1')
        self.assertEqual(user.profile,profile)

        