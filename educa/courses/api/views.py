import math
from os import stat
from rest_framework import viewsets,status
from ..models import Subject,Course,Module
from .serializers import SubjectSerializer,PublicCourseListSerializer,PublicCourseSerializer
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

class SubjectViewSet(viewsets.ViewSet):
    queryset = Subject.objects.all()
    
    def list(self,request):
        serializer = SubjectSerializer(self.queryset,many=True)
        return Response(serializer.data)

    def create(self,request):
        if request.user.is_authenticated:
            serializer = SubjectSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'message':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
    


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

        if 'subject_name' in kwargs:
            subject_name = kwargs['subject_name']
            if subject_name in [subject.slug for subject in Subject.objects.all() ]:
                output['subject_name'] = subject_name
                self.queryset = self.queryset.filter(subject__slug=subject_name)
            else:
                return Response({'massage':'Subject doesnot exist'},status=status.HTTP_404_NOT_FOUND)
        else:
            subject_name=None
        total_pages = self.get_total_pages(self.queryset)
        if self.page_number > total_pages or self.page_number < 1:
            return Response({'message':'Page number out of bound.'},status=status.HTTP_406_NOT_ACCEPTABLE)
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
    