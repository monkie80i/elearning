from django.urls import path
from .views import manage_course_view,course_create_view,course_update_view,course_delete_view,module_create_update_view,course_detail_view,module_delete_view,content_create_update_view,content_delete_view,manage_module_content_list,course_list_view,public_course_detail,course_enroll_view,student_course_detail_view,student_course_list_view,manage_course_preview,course_un_enroll_view

urlpatterns = [
    path('manage/course/list/<str:subject>/',manage_course_view,name='manage_course_list'),
    path('manage/course/create/',course_create_view,name = 'course_create'),
    path('manage/course/<int:id>/',course_detail_view,name='manage_course_detail'),
    path('manage/course/<int:id>/update/',course_update_view,name = 'course_update'),
    path('manage/course/<int:pk>/delete/',course_delete_view,name = 'course_delete'),
    path('manage/course/<int:course_id>/module/create/',module_create_update_view,name='create_module'),
    path('manage/course/<int:course_id>/module/<int:id>/update/',module_create_update_view,name='update_module'),
    path('manage/course/<int:course_id>/module/<int:pk>/delete/',module_delete_view,name='delete_module'),
    path('manage/module/<int:module_id>/content/<model_name>/create/',content_create_update_view,name='create_content'),
    path('manage/module/<int:module_id>/content/<model_name>/update/<id>',content_create_update_view,name='update_content'),
    path('manage/content/<int:content_id>/delete/',content_delete_view,name='delete_content'),
    path('manage/module/<int:module_id>/',manage_module_content_list,name='module_content_list'),
    path('manage/course/preview/<course_id>/',manage_course_preview,name='manage_course_preview_detail'),
    path('manage/course/preview/<course_id>/<module_id>/',manage_course_preview,name='manage_course_preview_detail_module'),
    path('',course_list_view,name='course_list'),
    path('subject/<slug:subject>/',course_list_view,name='course_list_subject'),
    path('course/<int:id>/',public_course_detail,name="public_course_detail"),
    path('enroll-course/',course_enroll_view,name="student_enroll_course"),
    path('enrolled/list/',student_course_list_view,name='student_course_list'),
    path('enrolled/course/<course_id>/',student_course_detail_view,name='student_course_detail'),
    path('enrolled/course/<course_id>/<module_id>/',student_course_detail_view,name='student_course_detail_module'),
    path('unenroll/<int:course_id>/',course_un_enroll_view,name='student_unenroll_course'),
]