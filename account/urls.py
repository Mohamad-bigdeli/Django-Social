from django.urls import path
from . import views
from .forms import *
from django.contrib.auth import views as auth_views


app_name="account"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='registration/login.html'), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('edit_user', views.EditUserView.as_view(), name="edit_user"),
    path('forget_password/', views.ForgetPasswordView.as_view(), name="forget_password"),
    path('send_mail_done/', views.send_mail_done, name="send_mail_done"),
    path('password_reset_confirm/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('users/', views.user_list, name="user_list"), 
    path('users/<username>', views.user_detail, name="user_detail"),
    path('follow/', views.user_follow, name="user_follow")
]