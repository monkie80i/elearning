from dis import dis
from functools import partial
import math
from os import stat
from django import dispatch
from rest_framework import viewsets,status
from ..models import Subject,Course,Module
from .serializers import SubjectSerializer,PublicCourseListSerializer,PublicCourseSerializer,CourseSerializer,ManageCourseMinSzr
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
from utils.helpers import get_object_or_404_json
from django.shortcuts import get_object_or_404
from .permissions import IsTeacher
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import APIException,NotFound,PermissionDenied

#helper functions
def has_subject_slug_in_parameter(*args, **kwargs):
    """IF there isa subject slug in kargs return it or else retutn 0"""
    if 'subject_slug' in kwargs:
        return kwargs['subject_slug']
    else:
        return None

def filter_course_by_subject(qs,subject_slug):
    """Filters a course queryset with respect to the subject slug provided
    """
    if subject_slug in [subject.slug for subject in Subject.objects.all() ]:
        qs = qs.filter(subject__slug=subject_slug)
    else:
        raise NotFound(detail="Subject doesnot exist",code = status.HTTP_404_NOT_FOUND)
    return qs  
#helper classes
class PaginateViewSetMixin(object):
    page_size = 3
    
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
    
 

class PaginateNewMIxin(object):
    page_size = 3 #default
    queryset = None
    paginated_qs = None
    page_number = 1
    outpu = {}

    def paginate(self,*args, **kwargs):
        """Thake a queryset or a list ,
        page_size is the number of item in one page,
        page_number starts from 1 to length of qs/page_size
        """
        if self.queryset is not None:
            # set page number
            if 'page_number' in kwargs:
                self.page_number = kwargs['page_number']
            else:
                self.page_number = 1
            #sets the total number of pages
            self.total_pages = math.ceil(self.queryset.count()/self.page_size)
            #paginate
            start = (self.page_number-1)*self.page_size
            end = self.page_number*self.page_size
            self.paginated_qs = self.queryset[start:end]
            self.output = {
                'page_number':self.page_number,
                'total_pages':self.total_pages
            }
            return self.paginated_qs
        

class SubjectViewSet(viewsets.ViewSet):
    queryset = Subject.objects.all()
    
    def list(self,request):
        serializer = SubjectSerializer(self.queryset,many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SubjectSerializer)
    def create(self,request):
        if request.user.is_authenticated:
            serializer = SubjectSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'detail':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
    


class CoursePublicViewSet(PaginateViewSetMixin,viewsets.ViewSet):
    queryset = Course.objects.all()
    serializer = PublicCourseListSerializer
    page_size = 5

    def list(self,request,*args, **kwargs):
        output = {}
        if 'page_number' in kwargs:
            self.page_number = kwargs['page_number']
        else:
            self.page_number = 1

        if 'subject_slug' in kwargs:
            subject_slug = kwargs['subject_slug']
            if subject_slug in [subject.slug for subject in Subject.objects.all() ]:
                output['subject_slug'] = subject_slug
                self.queryset = self.queryset.filter(subject__slug=subject_slug)
            else:
                return Response({'massage':'Subject doesnot exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            subject_slug=None
        total_pages = self.get_total_pages(self.queryset)
        if self.page_number > total_pages or self.page_number < 1:
            return Response({'detail':'Page number out of bound.'},status=status.HTTP_406_NOT_ACCEPTABLE)
        self.queryset = self.paginate(self.queryset)
        serializer = self.serializer(self.queryset,many=True)
        output['courses'] = serializer.data
        output['page_number'] = self.page_number
        output['total_pages'] = total_pages
        return Response(output,status=status.HTTP_200_OK)

    def retrieve(self,request,id=None):
        try:
            course = Course.objects.get(id=id)
        except:
            return Response({"mesage":"Course Does not exists."},status = status.HTTP_404_NOT_FOUND)
        serializer = PublicCourseSerializer(course)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
#Manage
def is_aiuthenticated_teacher(request):
    if request.user.is_authenticated:
        is_teacher = request.user.is_teacher
    else:
        is_teacher = False
    if is_teacher == True:
        return True
    else:
        raise PermissionDenied()



class ManageCourseViewSet(PaginateNewMIxin,viewsets.ViewSet):
    queryset = None
    permission_classes = [IsTeacher]
    page_size = 5

    def get_queryset(self,request):
        return Course.objects.filter(user= request.user)

    # for teacher
    def list(self,request,*args, **kwargs):
        self.queryset = self.get_queryset(request)
        subject_slug = has_subject_slug_in_parameter(*args, **kwargs)
        if subject_slug is not None:
            self.queryset = filter_course_by_subject(self.queryset,subject_slug)
        courses = self.paginate(*args, **kwargs)
        serializer = ManageCourseMinSzr(courses,many=True)
        self.output['courses'] = serializer.data
        return Response(self.output,status=status.HTTP_200_OK)

    def retrieve(self,request,id=None):
        course = get_object_or_404(Course,id=id,user=request.user)
        serializer = CourseSerializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)

    #from .schemas import CourseReadSerializer,CourseWriteSerializer
    @swagger_auto_schema(request_body=CourseSerializer)
    def create(self,request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=CourseSerializer)
    def update(self,request,id=None):
        course = get_object_or_404(Course,id=id,user=request.user)
        serializer = CourseSerializer(instance=course,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    
    @swagger_auto_schema(request_body=CourseSerializer)
    def partial_update(self,request,id=None):
        course = get_object_or_404(Course,id=id,user=request.user)
        serializer = CourseSerializer(instance=course,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_206_PARTIAL_CONTENT)

    def destroy(self,request,id=None):
        course = get_object_or_404_json(Course,id=id,user=request.user)
        try:
            course.delete()
        except Exception as e:
            return Response({'detail':e},status=status.HTTP_409_CONFLICT)
        return Response({'detail':'Course deleted'},status=status.HTTP_200_OK)


