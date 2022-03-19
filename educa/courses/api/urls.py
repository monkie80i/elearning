from django.urls import path
from .views import SubjectViewSet,CoursePublicViewSet,ManageCourseViewSet

app_name = 'courses'

urlpatterns = [
    path('subject/all/',SubjectViewSet.as_view({'get':'list'}),name="subject_list"),
    path('subject/create/',SubjectViewSet.as_view({'post':'create'}),name="subject_create"),
    path('courses/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all'),
    path('courses/<int:page_number>',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all_page'),
    path('courses/subject/<str:subject_name>/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject'),
    path('courses/subject/<str:subject_name>/<int:page_number>',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject_page'),
    path('course/<int:id>/',CoursePublicViewSet.as_view({'get':'retrieve'}),name='public_course_detail'),
    path('manage/courses/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list'),
    path('manage/course/',ManageCourseViewSet.as_view({'post':'create'}),name='manage_course_create'),
    path('manage/course/<int:id>/',ManageCourseViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'patch':'partial_update',
        'delete':'destroy'
    }),name='manage_course_detail_update_delete'),

]