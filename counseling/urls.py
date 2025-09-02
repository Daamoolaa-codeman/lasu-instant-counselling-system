from django import forms
from .models import Appointment
from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.view_appointment, name='view_appointments'),  # Match name exactly
    path('success/', views.appointment_success, name='appointment_success'),
    path('', views.render_homepage, name='render_homepage'),
    path('feedback/<int:appointment_id>/', views.submit_feedback, name='submit_feedback'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/counselor/', views.counselor_login, name='counselor_login'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/counselor/', views.counselor_signup, name='counselor_signup'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('counselor_dashboard/', views.counselor_dashboard, name='counselor_dashboard'),
    path('students_feedback/', views.students_feedback, name='students_feedback'),
    path('logout/', views.logout_view, name='logout'),
    path('about_counseling/', views.about_counseling, name='about_counseling'),
    path('videos/', views.video_list, name='video_list'),
    path('session-history/', views.render_session_history, name='session_history'),
]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counseling_service', 'date', 'time']
