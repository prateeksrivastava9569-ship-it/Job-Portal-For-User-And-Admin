"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from job.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('admin_login',admin_login,name="admin_login"),
    path('user_login',user_login,name="user_login"),
    path('recuiter_login',recuiter_login,name="recuiter_login"),
    path('user_signup',user_signup,name="user_signup"),
    path('user_home',user_home,name="user_home"),
    path('user_profile',user_profile,name="user_profile"),
    path('recuiter_signup',recuiter_signup,name="recuiter_signup"),
    path('admin_home',admin_home,name="admin_home"),
    path('recuiter_home',recuiter_home,name="recuiter_home"),
    path('recruiter_profile',recruiter_profile,name="recruiter_profile"),
    path('view_users',view_users,name="view_users"),
    path('recuiter_pending',recuiter_pending,name="recuiter_pending"),
    path('logout',logout,name="logout"),
    path('forgot_password',forgot_password,name="forgot_password"),
    path('verify_otp',verify_otp,name="verify_otp"),
    path('reset_password',reset_password,name="reset_password"),
    path('delete_user/<int:pid>',delete_user,name="delete_user"),
    path('change_status/<int:pid>',change_status,name="change_status"),
    path('recuiter_accepted', recuiter_accepted, name="recuiter_accepted"),
    path('recuiter_rejected', recuiter_rejected, name="recuiter_rejected"),
    path('recuiter_all', recuiter_all, name="recuiter_all"),
    path('delete_recuiter/<int:pid>',delete_recuiter,name="delete_recuiter"),
    path('change_passwordadmin',change_passwordadmin,name="change_passwordadmin"),
    path('change_passworduser',change_passworduser,name="change_passworduser"),
    path('change_passwordrecuiter',change_passwordrecuiter,name="change_passwordrecuiter"),
    path('add_job',add_job,name="add_job"),
    path('job_list',job_list,name="job_list"),
    path('edit_jobdetail/<int:pid>',edit_jobdetail,name="edit_jobdetail"),
    path('change_companylogo/<int:pid>',change_companylogo,name="change_companylogo"),
    path('view_job_user',view_job_user,name="view_job_user"),
    path('my_applied_jobs',my_applied_jobs,name="my_applied_jobs"),
    path('full_job_detail/<int:id>',full_job_detail,name="full_job_detail"),
    path('apply_now/<int:id>',apply_now,name="apply_now"),
    path('apply_success/<int:id>',apply_success,name="apply_success"),
    path('applyed_condidate',applyed_condidate,name="applyed_condidate"),
    path('applied_condidate_list',applied_condidate_list,name="applied_condidate_list"),
    path('change_application_status/<int:id>', change_application_status, name='change_application_status'),
    path('download_joining_letter/<int:id>', download_joining_letter, name='download_joining_letter'),
    path('candidate_detail/<int:id>', candidate_detail, name='candidate_detail'),
    path('application_history/<int:id>', application_history, name='application_history'),
    path('history_dashboard', application_history_dashboard, name='history_dashboard'),
    path('download_resume/<int:id>', download_resume, name='download_resume'),
    path('latest_job',latest_job,name="latest_job"),
    path('contact_us',contact_us,name="contact_us"),
    path('delete_job/<int:id>',delete_job,name="delete_job"),
    path('delete_condidate/<int:id>',delete_condidate,name="delete_condidate"),
    path('health/', health_check, name='health'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
