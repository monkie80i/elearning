from dataclasses import dataclass
from genericpath import exists
from .serializers import SubjectSerializer
from django.test import RequestFactory,TestCase,Client
from rest_framework.test import APIClient
from ..models import Subject,Course,Module,Content
from adminManager.models import User
import json,requests
from django.urls import reverse_lazy
import random
import math
from requests.auth import HTTPBasicAuth

class SubjectTestCase(TestCase):
    def setUp(self):
        subject1 = Subject(title="hindi")
        subject1.save()
        subject2 = Subject(title="english")
        subject2.save()
        subject3 = Subject(title="math")
        subject3.save()
        self.c = APIClient()
        user = User(username="admin")
        user.set_password("admin")
        user.save()

    
    def test_subject_list(self):
        response = self.c.get(reverse_lazy('api:subject_list'))
        self.assertEqual(response.status_code,200)
        print(json.loads(response.content))

    def test_creation_code(self):
        serializer = SubjectSerializer(data={'title':'java'})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(Subject.objects.all())

    def test_subject_create(self):
        data = {'title':'python'}
        self.c.login(username='admin',password='admin')
        response = self.c.post(reverse_lazy('api:subject_create'),data=data)
        print(response.content)
        #print(Subject.objects.get(title='python'))
        self.assertEqual(Subject.objects.all().filter(title='python').exists(),True)

class PublicCourseListTestCase(TestCase):
    def setUp(self):
        subjects = ['science','english','math','python',]
        for sub in subjects:
            s = Subject(title=sub.capitalize(),slug=sub)
            s.save()
        self.c = APIClient()
        users = {'teacher1':'teacher1234','student1':'student1234'}
        for uname,pwd in users.items():
            u = User(username=uname)
            u.set_password(pwd)
            u.save()
        all_users = User.objects.all()
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, non faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim sit amet leo."""
        for i in range(1,54):
            c = Course(
                title=f'Course {i}',
                overview=content,
                user = random.choice(all_users),
                subject=random.choice(all_subects)
            )
            c.save()
        print('subjects',all_subects)
        print('users',all_users)
    
    def test_course_list_all(self):
        total_pages = math.ceil(Course.objects.count()/5)
        url = reverse_lazy('api:public_course_list_all')
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(len(content['courses']),5)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],1)
    
    def test_course_list_page(self):
        # for first page
        total_pages = math.ceil(Course.objects.count()/5)
        url = reverse_lazy('api:public_course_list_all_page',args=[1])
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        self.assertEqual(len(content['courses']),5)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],1)
        # for Last page
        url = reverse_lazy('api:public_course_list_all_page',args=[total_pages])
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        #self.assertEqual(len(content['courses']),3)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],total_pages)
    
    def test_course_list_page_out_of_bound(self):
        # for first page
        url = reverse_lazy('api:public_course_list_all_page',args=[100])
        response = self.c.get(url)
        print(response.content)
        self.assertEqual(response.status_code,406)

    def test_course_list_subject(self):
        random_subject = random.choice(self.subjects)
        url = reverse_lazy('api:public_course_list_subject',args=[random_subject.slug])
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        print(content)
        courses_of_random_subject = Course.objects.filter(subject=random_subject)
        total_pages = math.ceil(courses_of_random_subject.count()/5)
        #self.assertEqual(len(content['courses']),Courses)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],1)
    
    def test_course_list_illegal_subject(self):
        # for first page
        url = url = reverse_lazy('api:public_course_list_subject',args=["illegal"])
        response = self.c.get(url)
        print(response.content)
        self.assertEqual(response.status_code,404)
    
    def test_course_list_subject_page(self):
        # for first page
        random_subject = random.choice(self.subjects)
        url = reverse_lazy('api:public_course_list_subject_page',args=[random_subject.slug,1])
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        print(content)
        courses_of_random_subject = Course.objects.filter(subject=random_subject)
        total_pages = math.ceil(courses_of_random_subject.count()/5)
        #self.assertEqual(len(content['courses']),Courses)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],1)
        # for last page
        random_subject = random.choice(self.subjects)
        courses_of_random_subject = Course.objects.filter(subject=random_subject)
        total_pages = math.ceil(courses_of_random_subject.count()/5)
        url = reverse_lazy('api:public_course_list_subject_page',args=[random_subject.slug,total_pages])
        response = self.c.get(url)
        self.assertEqual(response.status_code,200)
        content = json.loads(response.content)
        print(content)
        self.assertEqual(content['total_pages'],total_pages)
        self.assertEqual(content['page_number'],total_pages)

class PublicCourseDetailTestCase(TestCase):
    def setUp(self):
        subjects = ['science','english','math','python',]
        for sub in subjects:
            s = Subject(title=sub.capitalize(),slug=sub)
            s.save()
        self.c = APIClient()
        users = {'teacher1':'teacher1234','student1':'student1234'}
        for uname,pwd in users.items():
            u = User(username=uname)
            u.set_password(pwd)
            u.save()
        all_users = User.objects.all()
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, non faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim sit amet leo."""
        course = Course(title="Python 101",overview=content,subject = all_subects.filter(slug='python').first(),user=random.choice(all_users))
        course.save()
        for i in range(1,6):
            m = Module(title=f'Module {i}',description=content,course=course)
            m.save()
        print('subjects',all_subects)
        print('users',all_users)
        self.course_id = course.id

    def test_detail_view(self):
        url = reverse_lazy('api:public_course_detail',args=[self.course_id])
        print(url)
        response = self.c.get(url)
        data = json.loads(response.content)
        print(data['modules_count'])

        #self.assertEqual(response.status_code,200)
    
    """def test_detail_out_of_scope(self):
        response = self.c.get(reverse_lazy('api:public_course_detail',args=[21]))
        print(json.loads(response.content))
        self.assertEqual(response.status_code,404)
    """

class ManageCourseTestCase(TestCase):
    def setUp(self):
        subjects = ['science','english','math','python',]
        for sub in subjects:
            s = Subject(title=sub.capitalize(),slug=sub)
            s.save()
        self.c = APIClient()
        
        users = [
            {   
                'name':'teacher1',
                'password':'teacher1234',
                'is_teacher':True,
                'is_student':False,

            },
            {   
                'name':'student1',
                'password':'student1234',
                'is_teacher':False,
                'is_student':True,
            }
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        #self.c.session.headers.update({'x-test': 'true'})
        all_users = User.objects.all()
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, non faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim sit amet leo."""
        course1 = Course(title="Course 1",overview=content,subject = all_subects.filter(slug='python').first(),user=all_users[0])
        course2 = Course(title="Course 2",overview=content,subject = all_subects.filter(slug='python').first(),user=all_users[0])
        course1.save()
        course2.save()
        for i in range(1,6):
            m = Module(title=f'Module 1.{i}',description=content,course=course1)
            m.save()
        for i in range(1,4):
            m = Module(title=f'Module 2.{i}',description=content,course=course2)
            m.save()
        #print('subjects',all_subects)
        #print('users',all_users)

    def test_course_list(self):
        response = self.c.get(reverse_lazy('api:manage_course_list'))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,200)
    
    def test_course_list_anonymous(self):
        client = APIClient()
        response = client.get(reverse_lazy('api:manage_course_list'))
        data = json.loads(response.content)
        #print(data,response.status_code)
        self.assertEqual(response.status_code,401)
    
    def test_course_list_not_teacher(self):
        client = APIClient()
        cred = 'student1:student1234'
        import base64
        encoded_cred = base64.b64encode(cred.encode()).decode()
        print(encoded_cred)
        client.credentials(HTTP_AUTHORIZATION=f'Basic {encoded_cred}')
        response = client.get(reverse_lazy('api:manage_course_list'))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,403)

    def test_course_detail(self):
        response = self.c.get(reverse_lazy('api:manage_course_detail_update_delete',args=[1]))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,200)
    
    def test_course_detail_that_does_not_exists(self):
        response = self.c.get(reverse_lazy('api:manage_course_detail_update_delete',args=[3]))
        data = json.loads(response.content)
        #print(data,response.status_code)
        self.assertEqual(response.status_code,404)

    def test_course_create(self):
        data = {
            'subject_slug':'python',
            'title':'Course 3',
            'overview':'Brand new course'
        }
        response = self.c.post(reverse_lazy('api:manage_course_create'),data=data)
        resp = json.loads(response.content)
        self.assertEqual(Course.objects.filter(title=data['title']).exists(),True)
        #print(resp)
    
    def test_course_create_blank_data(self):
        data = {}
        prev_course_count = Course.objects.count()
        response = self.c.post(reverse_lazy('api:manage_course_create'),data=data)
        resp = json.loads(response.content)
        self.assertEqual(Course.objects.count(),prev_course_count)
        #print(resp)
    
    def test_course_create_only_subject(self):
        prev_course_count = Course.objects.count()
        data = {
            'subject_slug':'python'
        }
        response = self.c.post(reverse_lazy('api:manage_course_create'),data=data)
        resp = json.loads(response.content)
        self.assertEqual(Course.objects.count(),prev_course_count)
        #print(resp,response.status_code)

    def test_course_create_invalid_subject(self):
        data = {
            'subject_slug':'pyth',
            'title':'Course 3',
            'overview':'Brand new course'
        }
        response = self.c.post(reverse_lazy('api:manage_course_create'),data=data)
        self.assertEqual(response.status_code,400)
        #print(response.content,response.status_code)

    def test_course_update_full_data(self):
        course = Course.objects.get(id=1)
        data = {
            'title':course.title,
            'subject_slug': course.subject.slug,
            'overview':'New Overview'
        }
        #print(data)
        response = self.c.put(reverse_lazy('api:manage_course_detail_update_delete',args=[1]),data=data)
        #print(json.loads(response.content))
        course = Course.objects.get(id=1)
        self.assertEqual(course.overview,data['overview'])
    
    def test_course_update_object_doesnot_exist(self):
        course = Course.objects.get(id=1)
        data = {
            'title':course.title,
            'subject_slug': course.subject.slug,
            'overview':'New Overview'
        }
        #print(data)
        response = self.c.put(reverse_lazy('api:manage_course_detail_update_delete',args=[5]),data=data)
        #print(json.loads(response.content))
        #self.assertEqual(res,data['overview'])

    def test_course_update_partial(self):
        course = Course.objects.get(id=1)
        data = {
            'overview':'New Overview'
        }
        #print(data)
        response = self.c.patch(reverse_lazy('api:manage_course_detail_update_delete',args=[1]),data=data)
        #print(json.loads(response.content))
        course = Course.objects.get(id=1)
        self.assertEqual(course.overview,data['overview'])

    def test_course_delete(self):
        course = Course.objects.get(id=1)
        response = self.c.delete(reverse_lazy('api:manage_course_detail_update_delete',args=[1]))
        #print(json.loads(response.content))
        self.assertEqual(Course.objects.filter(id=1).exists(),False)

class ManageCourseListPaginationTestCase(TestCase):
    def setUp(self):
        subjects = ['science','english','math','python',]
        for sub in subjects:
            s = Subject(title=sub.capitalize(),slug=sub)
            s.save()
        self.c = APIClient()
        
        users = [
            {   
                'name':'teacher1',
                'password':'teacher1234',
                'is_teacher':True,
                'is_student':False,

            },
            {   
                'name':'student1',
                'password':'student1234',
                'is_teacher':False,
                'is_student':True,
            }
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        teacher = all_users.filter(is_teacher=True).first()
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        #self.c.session.headers.update({'x-test': 'true'})
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, non faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim sit amet leo."""
        for i in range(1,54):
            c = Course(
                title=f'Course {i}',
                overview=content,
                user = teacher,
                subject=random.choice(all_subects)
            )
            c.save()
        self.total_pages = math.ceil(Course.objects.filter(user=teacher).count()/5)
        print('total_pages',self.total_pages)
        

    def test_course_list(self):
        response = self.c.get(reverse_lazy('api:manage_course_list'))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data['courses']),5)
        self.assertEqual(data['total_pages'],self.total_pages)
        self.assertEqual(data['page_number'],1)
    
    def test_course_list_page(self):
        response = self.c.get(reverse_lazy('api:manage_course_list_page',args=[1]))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data['courses']),5)
        self.assertEqual(data['total_pages'],self.total_pages)
        self.assertEqual(data['page_number'],1)

    def test_course_list_page_last(self):
        response = self.c.get(reverse_lazy('api:manage_course_list_page',args=[self.total_pages]))
        data = json.loads(response.content)
        #print(data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(data['courses']),3)
        self.assertEqual(data['total_pages'],self.total_pages)
        self.assertEqual(data['page_number'],self.total_pages)
