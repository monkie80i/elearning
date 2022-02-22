from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase,Client
from .views import user_registration_view as uv
from .models import User
from django.urls import reverse,reverse_lazy
from django.conf import settings

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