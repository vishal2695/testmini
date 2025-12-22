"""mini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogg import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.usersignup, name='signup'),
    path('', views.userlogin, name='login'),
    path('log/', views.userlogout, name='logout'),
    path('dashboard/', views.dashboardd, name='dashboard'),
    path('add/', views.addblog, name='add'),
    path('update/<int:id>/', views.updateblog, name='update'),
    path('delete/<int:id>/', views.deleteblog, name='delete'),
    path('password/', views.passwordchange, name='password'),
    path('details/', views.detail, name='details'),
    path('change/<int:id>/', views.updatedetail, name='datachange'),
    path('deletedata/<int:id>/', views.deletedetail, name='deletedetail'),
    path('search/', views.search, name='search'), 
    path('profile/', views.profiles, name='profile'),
    path('show/<int:id>/', views.showpage, name='show'),
    path('like/<int:id>',views.like_blog, name='likes'),
    path('comdelete/<int:id>',views.comdelete, name='comdelete'),
    path('dp/',views.dpfile, name='dp'),
    path('search_blogg/', views.searchblogg ,name='searchblogg'),




    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html'),
     name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_sent.html'),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_form.html'),
     name='password_reset_confirm'),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_done.html'),
    name='password_reset_complete'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

