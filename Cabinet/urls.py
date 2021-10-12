"""Cabinet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from Doctor import views as v
from django.contrib.auth import views as auth_views


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', v.welcome,name='Welcome-index'),
    url(r'^signinuser/$', v.signinuser,name='inscription'),
    url(r'^login/$',v.loginview,name='patientlogin'),
    url('afterlog/(?P<pk>[-\w\x20]+)',v.afterlogin,name='afterlogin'),
    url('dashboard/(?P<pk>[-\w\x20]+)',v.PatientDash1,name='Firstdash'),
    url('dashboard2/(?P<pk>[-\w\x20]+)',v.PatientDash2,name='rendez_vous_dash'),
    url('dashboard3/(?P<pk>[-\w\x20]+)',v.PatientDash3,name='assurance_dash'),
    url('logout', v.logoutUser, name="logout"),
    url('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url('reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/', auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    url('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url('doctordash1', v.DoctorDash1, name='docdash1'),
    url('doctordash2', v.DoctorDash2, name='docdash2'),
    url('doctordash3', v.DoctorDash3, name='docdash3'),
    url('doctordash4', v.DoctorDash4, name='docdash4'),
    url('doctordash5', v.DoctorDash5, name='docdash5'),
    url('doctordash6', v.DoctorDash6, name='docdash6'),
    url('doctordash7', v.DoctorDash7, name='docdash7'),
    url('doctordash8', v.DoctorDash8, name='docdash8'),
    url('doctordash9', v.DoctorDash9, name='docdash9'),
    url('edit-patient/(?P<pk>[-\w\x20]+)', v.edit_patient, name='editpatient'),
    url('delete-patient/(?P<pk>[-\w\x20]+)', v.delete_patient, name='deletepatient'),
    url('delete-certif/(?P<pk>[-\w\x20]+)', v.delete_certif, name='deletecertif'),
    url('delete-medic/(?P<pk>[-\w\x20]+)', v.delete_medic, name='deletemedic'),
    url('payer/(?P<pk>[-\w\x20]+)', v.payer, name='payer'),
]
