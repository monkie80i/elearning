from .serializers import SubjectSerializer,ModuleSerializer,ContentSerializer
from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Subject,Course,Module,Content,Text,Image,Video,File
from adminManager.models import User
import json
from django.urls import reverse_lazy
import random
import math,os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

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

from .serializers import  TextSerializer,ImageSerializer,FileSerializer,VideoSerializer
content_serializer = {
    'text': TextSerializer,
    'image': ImageSerializer,
    'file': FileSerializer,
    'video':VideoSerializer
}

class ContentSerializerTestCase(TestCase):
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
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        teacher = all_users.filter(is_teacher=True).first()
        self.teacher = teacher
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, 
        on faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. 
        Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor
         venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim 
         sit amet leo."""
        course = Course(
            title='Course 1',
            overview=content,
            user = teacher,
            subject=random.choice(all_subects)
        )
        course.save()
        self.module = Module(
            title="Module 1",
            description=content,
            course=course
        )
        self.module.save()
    
    def test_create_content_text(self):
        print(self.module.contents.all())

        content_type='text'
        data = {
            'title':'Greeting',
            'content':' hai ther How are you'
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher)
        print(serializer.data)
        print(type(instance))
        content = Content(module=self.module,item=instance)
        content.save()
        self.assertEqual(self.module.contents.all()[0].item,instance)

    
    def test_create_content_image(self):
        print(self.module.contents.all())
        image = SimpleUploadedFile(r'C:\Users\ZAHN_PC\Documents\GitHub\Portfolio\egyan_templates\EGYAN_TEMPLATES\assets\images\socreatese.jpg', b"file_content", content_type="video/mp4")
        content_type='image'
        data = {
            'title':'My Image',
            'file':image
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher)
        print(serializer.data)
        print(type(instance))
        content = Content(module=self.module,item=instance)
        content.save()
        self.assertEqual(self.module.contents.all()[0].item,instance)

class ManageModuleTestCase(TestCase):
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
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        teacher = all_users.filter(is_teacher=True).first()
        self.teacher = teacher
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, 
        on faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. 
        Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor
         venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim 
         sit amet leo."""
        self.course = Course(
            title='Course 1',
            overview=content,
            user = teacher,
            subject=random.choice(all_subects)
        )
        self.course.save()
    
    def create_text_content(self,module,title=None,content=None):
        content_type='text'
        if title is None:
            title = "Greeting"
        if content is None:
            content = "hai ther How are you"
        data = {
            'title':title,
            'content':content
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher)
        #print(serializer.data)
        #print(type(instance))
        content = Content(module=module,item=instance)
        content.save()

    def test_module_create(self):
        data = {
            'title':'Module 1',
            'description':'Lorem'
        }
        resp = self.c.post(reverse_lazy('api:manage_module_create',args=[self.course.id]),data=data)
        response = json.loads(resp.content)
        #print(response,resp.status_code)
        self.assertEqual(201,resp.status_code)


    def test_module_order_working(self):
        data = {
            'title':'Module 1',
            'description':'Lorem'
        }
        resp = self.c.post(reverse_lazy('api:manage_module_create',args=[self.course.id]),data=data)
        response1 = json.loads(resp.content)
        
        data = {
            'title':'Module 2',
            'description':'Lorem'
        }
        resp = self.c.post(reverse_lazy('api:manage_module_create',args=[self.course.id]),data=data)
        response2 = json.loads(resp.content)
        self.assertEqual(response1.order+1,response2.order)
    
    def test_module_create_wrong_key(self):
        data = {
            'title':'Module 1',
            'descriptio':'Lorem'
        }
        resp = self.c.post(reverse_lazy('api:manage_module_create',args=[self.course.id]),data=data)
        response = json.loads(resp.content)
        #print(response,resp.status_code)
        self.assertEqual(400,resp.status_code)
    
    def test_module_detail(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        self.create_text_content(module,title='Hello 1',content="Do well")
        self.create_text_content(module,title='Hello 2',content="Do well")
        self.create_text_content(module,title='Hello 3',content="Do well")
        resp = self.c.get(reverse_lazy('api:manage_module_detail',args=[module.id]))
        response = json.loads(resp.content)
        print(response,resp.status_code)
    
    def test_module_update(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        data = {
            'title':'Module 2',
            'description':'NOt lorem'
        }
        resp = self.c.put(reverse_lazy('api:manage_module_detail',args=[module.id]),data=data)
        response = json.loads(resp.content)
        #print(response,resp.status_code)
        module = Module.objects.get(id=module.id)
        self.assertEqual(module.title,data['title'])
    
    def test_module_update_with_insufficient_data(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        data = {
            'title':'Module 2',
            'descriptio':'NOt lorem'
        }
        resp = self.c.put(reverse_lazy('api:manage_module_detail',args=[module.id]),data=data)
        response = json.loads(resp.content)
        print(response,resp.status_code)
        #module = Module.objects.get(id=module.id)
        self.assertEqual(resp.status_code,400)
        
    def test_module_partial_update(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        data = {
            'title':'Module 2',
        }
        resp = self.c.patch(reverse_lazy('api:manage_module_detail',args=[module.id]),data=data)
        response = json.loads(resp.content)
        #print(response,resp.status_code)
        #module = Module.objects.get(id=module.id)
        self.assertEqual(module.title,data['title'])
        self.assertEqual(resp.status_code,206)


    def test_module_delete(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        resp = self.c.delete(reverse_lazy('api:manage_module_detail',args=[module.id]))
        response = json.loads(resp.content)
        print(response,resp.status_code)

    def test_module_with_content_delete(self):
        module = Module(
            title='Module 1',
            description="Lorem",
            course = self.course
        )
        module.save()
        self.create_text_content(module,title='Hello 1',content="Do well")
        self.create_text_content(module,title='Hello 2',content="Do well")
        self.create_text_content(module,title='Hello 3',content="Do well")
        ser = ModuleSerializer(module)
        #print(ser.data)
        resp = self.c.delete(reverse_lazy('api:manage_module_detail',args=[module.id]))
        response = json.loads(resp.content)
        #print(response,resp.status_code)
        self.assertEqual(resp.status_code,200)

#test serializer for each item type
#test serializer for each item type with less fields,without partial
#test serializer for each item type with less fields,with partial
#test api end point for each item type,with less fields
#check if after updatio of item, the user is still there or not and also the content
class MyTestCase(TestCase):

    def get_default_image(self):
        fp = settings.BASE_DIR / 'test_medias' / 'image.jpg'
        return os.fspath(fp.resolve())

    def get_default_image_path(self):
        return SimpleUploadedFile(self.get_default_image(), b"file_content", content_type="image/jpg")

    def get_default_file(self):
        fp = settings.BASE_DIR / 'test_medias' / 'file.scss'
        return os.fspath(fp.resolve())
    
    def get_default_file_path(self):
        return SimpleUploadedFile(self.get_default_file(), b"file_content", content_type="text/scss")

    def get_default_url(self):
        return 'https://www.google.com'

    def creat_course(self,owner,title=None,content=None):
        if title is None:
            title='Course 1'
        if content is None:
            content = 'Lorem Not my fucking problem.'
        course = Course(
            title=title,
            overview=content,
            user = owner,
            subject=random.choice(Subject.objects.all())
        )
        course.save()
        return course

    def create_module(self,course,title=None,description=None):
        if title is None:
            title='Course 1'
        if description is None:
            description = 'Lorem Not my fucking problem.'
        module = Module(
            title=title,
            description=description,
            course = course
        )
        module.save()
        return module

    def create_text_content(self,module,title=None,content=None):
        content_type='text'
        if title is None:
            title = "Greeting"
        if content is None:
            content = "hai ther How are you"
        data = {
            'title':title,
            'content':content
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher)
        #print(serializer.data)
        #print(type(instance))
        content = Content(module=module,item=instance)
        content.save()
        return content
    
    def create_image_content(self,module,title=None,file_name=None):
        #print(self.module.contents.all())
        content_type='image'
        if title is None:
            title = "My Image"
        if file_name is None:
            file_name = self.get_default_image()
        image = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        content_type='image'
        data = {
            'title':title,
            'file':image
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher)
        #print(serializer.data)
        #print(type(instance))  
        content = Content(module=module,item=instance)
        content.save()
        return content

    def create_file_content(self,module,title=None,file_name=None):
        #print(self.module.contents.all())
        content_type='file'
        if title is None:
            title = "My File"
        if file_name is None:
            file_name = self.get_default_file()
        #print(file_name)
        file = SimpleUploadedFile(file_name, b"file_content", content_type="video/mp4")
        data = {
            'title':title,
            'file':file
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher) 
        content = Content(module=module,item=instance)
        content.save()
        return content

    def create_video_content(self,module,title=None,file_name=None):
        #print(self.module.contents.all())
        content_type='video'
        if title is None:
            title = "Video 1"
        if file_name is None:
            url = self.get_default_url()
        #print(file_name)
        data = {
            'title':title,
            'url':url
        }
        serializer = content_serializer[content_type](data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(owner=self.teacher) 
        content = Content(module=module,item=instance)
        content.save()
        return content
    
    

class SerializerInspTestCase(MyTestCase):
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
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        self.teacher = all_users.filter(is_teacher=True).first()
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        self.all_subects = Subject.objects.all()
        self.lorem = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, 
        on faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. 
        Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor
         venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim 
         sit amet leo."""
        self.course = self.creat_course(self.teacher,'Course 1',self.lorem)
        self.module = self.create_module(self.course,'Module 1',self.lorem[:20])
    
    def test_module_ser(self):
        ser = ModuleSerializer()
        print(repr(ser))
    
    def test_text_serializer(self):
        ser = TextSerializer()
        print(repr(ser))
    
    def test_image_serializer(self):
        image_content = self.create_image_content(self.module,'test_image')
        ser = ImageSerializer(image_content.item)
        print(image_content.item.file.url)

    def test_file_serializer(self):
        file_content = self.create_file_content(self.module,'test_file')
        ser = FileSerializer(file_content.item)
        print(ser.data)
    
    def test_video_serializer(self):
        video_content = self.create_video_content(self.module,'test_vid')
        ser = VideoSerializer(video_content.item)
        print(ser.data)
    
    def test_content_serializer(self):
        file_content = self.create_file_content(self.module,'test_file')
        ser = ContentSerializer(file_content)
        print(ser.data)
    
    def test_content_update_text(self):
        item = self.create_text_content(self.module,title='Text1').item
        #print(item)
        #print(content_serializer['text'](item).data)
        newitem = {
            'title':'Newo',
            'content':'new'
        }
        serializer = content_serializer['text'](data=newitem,instance=item)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        item = Text.objects.get(id=item.id)
        self.assertEqual(item.title,newitem['title'])
        self.assertEqual(item.content,newitem['content'])

    def test_content_update_file(self):
        item = self.create_file_content(self.module,title='File1').item
        #print(item)
        old = content_serializer['file'](item).data.copy()
        file = SimpleUploadedFile(self.get_default_image(), b"file_content", content_type="video/mp4")
        newitem = {
            'title':"new",
            'file':file
        }
        serializer = content_serializer['file'](data=newitem,instance=item)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #print(serializer.data)
        nitem = File.objects.get(id=item.id)
        self.assertEqual(nitem.title,newitem['title'])
        self.assertNotEqual(old['file'],serializer.data['file'])

class ManageContentTestCase(MyTestCase):
    
        
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
        ]
        for user in users:
            u = User(username=user['name'],is_teacher=user['is_teacher'],is_student=user['is_student'])
            u.set_password(user['password'])
            u.save()
        all_users = User.objects.all()
        teacher = all_users.filter(is_teacher=True).first()
        self.teacher = teacher
        self.c.credentials(HTTP_AUTHORIZATION='Basic dGVhY2hlcjE6dGVhY2hlcjEyMzQ=')
        all_subects = Subject.objects.all()
        self.subjects = all_subects
        content = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Quisque rhoncus, leo at dictum sollicitudin, sapien dolor vestibulum velit, 
        on faucibus ipsum est at tellus. Maecenas sed pharetra mi. Mauris eget turpis ante. 
        Cras et dignissim nisi. Phasellus commodo id mauris et suscipit. Ut in tellus a dolor
         venenatis mollis nec eu urna. Aenean massa nisl, accumsan ut vehicula ac, dignissim 
         sit amet leo."""
        self.course1 = self.creat_course(teacher,title='Course 1',content=content)

    def test_content_list(self):
        module = self.create_module(title='Module 101',course=self.course1)
        for i in range(5):
            self.create_text_content(module=module,title =f'Content {i}')
        m = Module.objects.get(id=module.id)
        ser = ModuleSerializer(m)
        resp = self.c.get(reverse_lazy('api:manage_content_list',args=[m.id]))
        response = json.loads(resp.content)
        self.assertEqual(resp.statuse_code,200)
        #print(json.dumps(response,indent=4),resp.status_code)
    
    def test_content_text_create(self):
        module = self.create_module(title='Module 101',course=self.course1)
        data = {
            'content': 'Poyedaa'
        }
        resp = self.c.post(reverse_lazy('api:manage_content_create',args=[module.id,'text']),data=data)
        response1 = json.loads(resp.content)
        #print(json.dumps(response1,indent=4),resp.status_code)
        resp = self.c.get(reverse_lazy('api:manage_content_list',args=[module.id]))
        response2 = json.loads(resp.content)
        #print(json.dumps(response,indent=4),resp.status_code)
        self.assertEqual(response1,response2["contents"][0])

    def test_content_all_create(self):
        module = self.create_module(title='Module 101',course=self.course1)
        #preparing data
        from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
        image = self.get_default_image_path()
        file = self.get_default_file_path()
        text_data = {
            'title':'My Text',
            'content': 'Poyedaa'
        }
        image_data = encode_multipart(BOUNDARY, {
            'title':'My Image',
            'file': image
        })

        file_data = encode_multipart(BOUNDARY, {
            'title':'My File',
            'file': file
        })
        video_data = {
            'title':'My Video',
            'url': self.get_default_url()
        }
        my_contents = []
        #create text
        resp = self.c.post(reverse_lazy('api:manage_content_create',args=[module.id,'text']),data=text_data)
        response_text = json.loads(resp.content)
        my_contents.append(response_text)
        #print(json.dumps(response_text,indent=4),resp.status_code)
        
        #create File
        resp = self.c.post(reverse_lazy('api:manage_content_create',args=[module.id,'file']),data=file_data,content_type=MULTIPART_CONTENT)
        response_file = json.loads(resp.content)
        print(resp.content,resp.status_code)
        #print(json.dumps(response_file,indent=4),resp.status_code)
        my_contents.append(response_file)


        #create Image
        resp = self.c.post(reverse_lazy('api:manage_content_create',args=[module.id,'image']),data=image_data,content_type=MULTIPART_CONTENT)
        response_image = json.loads(resp.content)
        print(resp.content,resp.status_code)
        #print(json.dumps(response_image,indent=4),resp.status_code)
        my_contents.append(response_image)

        #create Video
        resp = self.c.post(reverse_lazy('api:manage_content_create',args=[module.id,'video']),data=video_data)
        response_video = json.loads(resp.content)
        print(resp.content,resp.status_code)
        #print(json.dumps(response_video,indent=4),resp.status_code)
        my_contents.append(response_video)


        resp = self.c.get(reverse_lazy('api:manage_content_list',args=[module.id]))
        response2 = json.loads(resp.content)
        #print(json.dumps(response,indent=4),resp.status_code)
        self.assertEqual(my_contents,response2["contents"])

    def test_open_file(self):
        fp = settings.BASE_DIR / 'test_medias' / 'image.jpg'
        #os.path.join(fp.resolve())
        fp.read_bytes()