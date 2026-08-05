from django.urls import path
from . import views
urlpatterns = [path("login/",views.user_login,name="login"),
               path("home/",views.user_home,name='user_home'),
               path('register/',views.register,name='register'),
               path('logout/',views.user_logout,name='logout'),
               path('profile/',views.profile,name='profile'),
               path("forgot-password/", views.forgot_password, name="forgot_password"),
               path("change-password/", views.change_password, name="change_password"),
]
