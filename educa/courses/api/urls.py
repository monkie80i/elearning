from django.urls import path
from .views import OrderingViewSet, StudentViewSet, SubjectViewSet,CoursePublicViewSet,ManageCourseViewSet,ManageModuleCreate,ManageModuleDetail,ManageContentList,ManageContentDetail,EnrollmentViewset,OrderingViewSet

app_name = 'courses'

urlpatterns = [
    path('subjects/',SubjectViewSet.as_view(),name="subjects"),
    path('courses/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all'),
    path('courses/<int:page_number>/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_all_page'),
    path('courses/subject/<str:subject_slug>/',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject'),
    path('courses/subject/<str:subject_slug>/<int:page_number>',CoursePublicViewSet.as_view({'get':'list'}),name='public_course_list_subject_page'),
    path('course/<int:course_id>/',CoursePublicViewSet.as_view({'get':'retrieve'}),name='public_course_detail'),
    path('manage/courses/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list'),
    path('manage/courses/<int:page_number>/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_page'),
    path('manage/courses/subject/<str:subject_slug>/',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_subject'),
    path('manage/courses/subject/<str:subject_slug>/<int:page_number>',ManageCourseViewSet.as_view({'get':'list'}),name='manage_course_list_subject_page'),
    path('manage/course/',ManageCourseViewSet.as_view({'post':'create'}),name='manage_course_create'),
    path('manage/course/<int:course_id>/',ManageCourseViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'patch':'partial_update',
        'delete':'destroy'
    }),name='manage_course_detail_update_delete'),
    path('manage/course/<int:course_id>/module/',ManageModuleCreate.as_view(),name='manage_module_create'),
    path('manage/module/<int:module_id>/',ManageModuleDetail.as_view(),name='manage_module_detail'),
    path('manage/module/<int:module_id>/content/',ManageContentList.as_view({'get':'list'}),name='manage_content_list'),
    #path('manage/module/<int:module_id>/content/<str:content_type>/',ManageContentList.as_view({'post':'create'}),name='manage_content_create'),
    # create content
    path('manage/module/<int:module_id>/content/text/',ManageContentList.as_view({'post':'text_create'}),name='manage_content_create_text'),
    path('manage/module/<int:module_id>/content/image/',ManageContentList.as_view({'post':'image_create'}),name='manage_content_create_image'),
    path('manage/module/<int:module_id>/content/file/',ManageContentList.as_view({'post':'file_create'}),name='manage_content_create_file'),
    path('manage/module/<int:module_id>/content/video/',ManageContentList.as_view({'post':'video_create'}),name='manage_content_create_video'),
    #Content update and delete
    path('manage/content/text/<int:content_id>/',ManageContentDetail.as_view(
        {'put':'text_update'}
    ),name='manage_content_update_text'),
    path('manage/content/image/<int:content_id>/',ManageContentDetail.as_view(
        {'put':'image_update'}
    ),name='manage_content_update_image'),
    path('manage/content/file/<int:content_id>/',ManageContentDetail.as_view(
        {'put':'file_update'}
    ),name='manage_content_update_file'),
    path('manage/content/video/<int:content_id>/',ManageContentDetail.as_view(
        {'put':'video_update'}
    ),name='manage_content_update_video'),
    path('manage/content/<str:content_type>/<int:content_id>/',ManageContentDetail.as_view({'delete':'destroy'}),name='manage_content_delete'),
    #student
    path('enrolled/courses/',StudentViewSet.as_view({'get':'list_enrolled'}),name='enrolled_course_list'),
    path('enrolled/courses/<int:page_number>/',StudentViewSet.as_view({'get':'list_enrolled'}),name='enrolled_course_list_page'),
    path('enrolled/course/<int:course_id>/',StudentViewSet.as_view({'get':'course_detail'}),name='enrolled_course_detail'),
    path('enrolled/course/module/<int:module_id>/',StudentViewSet.as_view({'get':'module_content_list'}),name='enrolled_module_detail'),
    path('course/enroll/<int:course_id>',EnrollmentViewset.as_view({'get':'enroll'}),name='course_enroll'),
    path('course/unenroll/<int:course_id>',EnrollmentViewset.as_view({'get':'unenroll'}),name='course_unenroll'),
    path('manage/reorder/module/',OrderingViewSet.as_view({'post':'module'}),name='module_reorder'),
    path('manage/reorder/content/',OrderingViewSet.as_view({'post':'content'}),name='content_reorder'),
]