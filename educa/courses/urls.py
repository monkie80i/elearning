from django.urls import path
from .views import manage_course_view,course_create_view,course_update_view,course_delete_view,module_create_update_view,course_detail_view,module_delete_view,content_create_update_view,content_delete_view

urlpatterns = [
    path('course/list/<str:subject>/',manage_course_view,name='course_list'),
    path('course/<id>/',course_detail_view,name='course_detail'),
    path('course/create/',course_create_view,name = 'course_create'),
    path('course/<int:id>/update/',course_update_view,name = 'course_update'),
    path('course/<pk>/delete/',course_delete_view,name = 'course_delete'),
    path('course/<course_id>/module/create/',module_create_update_view,name='create_module'),
    path('course/<course_id>/module/<id>/update/',module_create_update_view,name='update_module'),
    path('course/<course_id>/module/<pk>/delete/',module_delete_view,name='delete_module'),
    path('module/<module_id>/content/<model_name>/create/',content_create_update_view,name='create_content'),
    path('module/<module_id>/content/<model_name>/create/<id>',content_create_update_view,name='update_content'),
    path('content/<content_id>/delete/',content_delete_view,name='delete_content'),

]