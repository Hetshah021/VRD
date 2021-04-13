from django.urls import path
from home.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('/', index, name='index'),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('profile/', profile.as_view(), name="profile"),
    path('<int:id>/profile_update/', profile_update, name='profile_update'),
    path('<int:id>/change_password/', change_password, name='change_password'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name = "password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"),
         name='password_reset_complete'),
]