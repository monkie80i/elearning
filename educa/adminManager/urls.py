from unicodedata import name
from django.urls import path,include
from .views import user_registration_view,user_home_view
from django.contrib.auth.views import LoginView,LogoutView

login_view = LoginView.as_view()
logout_view = LogoutView.as_view()
urlpatterns = [
    path('<user_type>/register/',user_registration_view,name='user_registration'),
    path('home/',user_home_view,name='user_home'),
    path('',login_view,name='login'),
    path('logout/',logout_view,name='logout'),

]