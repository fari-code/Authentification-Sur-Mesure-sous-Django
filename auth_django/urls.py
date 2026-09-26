from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.register,name='register'),
    path("login/",views.login,name='login'),
    path("forgot_password/",views.password_reset,name='password_reset'),
    path("dashboard/",views.dashboard,name='dashboard'),


]