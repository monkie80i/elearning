from unicodedata import name
from django.urls import path,include,reverse_lazy
from .views import user_registration_view,user_home_view,user_profile_private_view
from django.contrib.auth.views import LoginView,LogoutView

login_view = LoginView.as_view(next_page=reverse_lazy('user_home'))
logout_view = LogoutView.as_view()
urlpatterns = [
    path('<user_type>/register/',user_registration_view,name='user_registration'),
    path('profile/',user_profile_private_view,name='user_profile_private'),
    path('home/',user_home_view,name='user_home'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),

]