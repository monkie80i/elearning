from .serializers import SubjectSerializer
from django.test import RequestFactory,TestCase,Client
from rest_framework.test import APIClient
from ..models import Subject,Course,Module,Content
from adminManager.models import User
import json,requests
from django.urls import reverse_lazy
import random
import math

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