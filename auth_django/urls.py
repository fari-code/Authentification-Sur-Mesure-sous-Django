from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.register,name='register'),
    path("login/",views.login,name='login'),
    path("forgot_password/",views.password_reset,name='password_reset'),
    path("reset-password/<str:token>/", views.password_reset_confirm, name="reset-password"),
    path("dashboard/",views.dashboard,name='dashboard'),
    path("logout/",views.logout_view,name='logout'),
    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
]