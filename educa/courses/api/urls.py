from django.urls import path
from .views import SubjectViewSet,CoursePublicViewSet,ManageCourseViewSet,ManageModuleCreate,ManageModuleDetail

app_name = 'courses'

urlpatterns = [
    path('subjects/',SubjectViewSet.as_view({'get':'list'}),name="subject_list"),
    path('subject/create/',SubjectViewSet.as_view({'post':'create'}),name="subject_create"),
    path('courses/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all'),
    path('courses/<int:page_number>/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all_page'),
    path('courses/subject/<str:subject_slug>/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject'),
    path('courses/subject/<str:subject_slug>/<int:page_number>',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject_page'),
    path('course/<int:id>/',CoursePublicViewSet.as_view({'get':'retrieve'}),name='public_course_detail'),
    path('manage/courses/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list'),
    path('manage/courses/<int:page_number>/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_page'),
    path('manage/courses/subject/<str:subject_slug>/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_subject'),
    path('manage/courses/subject/<str:subject_slug>/<int:page_number>',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_subject_page'),
    path('manage/course/',ManageCourseViewSet.as_view({'post':'create'}),name='manage_course_create'),
    path('manage/course/<int:id>/',ManageCourseViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'patch':'partial_update',
        'delete':'destroy'
    }),name='manage_course_detail_update_delete'),
    path('manage/module/<int:course_id>/',ManageModuleCreate.as_view(),name='manage_module_create'),
    path('manage/module/detail/<int:id>/',ManageModuleDetail.as_view(),name='manage_module_detail'),

]