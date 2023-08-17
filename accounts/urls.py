from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register,name='register'),
    path('profile/',views.profile,name='profile'),
    path('update_profile/',views.update_profile,name='update_profile'),
    path('explore/',views.explore,name='explore'),
    path('login/',auth_view.LoginView.as_view(template_name='accounts/login.html'),name="login"),
    path('logout/',auth_view.LogoutView.as_view(template_name='accounts/logout.html'),name="logout"),
    path('user_profile/(?P<username>[a-zA-Z0-9]+)$',views.user_profile,name="user_profile"),
]
