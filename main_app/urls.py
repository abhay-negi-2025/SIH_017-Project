from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.welcome, name='welcome'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/<str:user_type>/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Alumni URLs
    path('alumni/dashboard/', views.alumni_dashboard, name='alumni_dashboard'),
    path('alumni/search/', views.alumni_search, name='alumni_search'),
    path('alumni/donations/', views.alumni_donations, name='alumni_donations'),
    path('alumni/events/', views.alumni_events, name='alumni_events'),
    path('alumni/mentorship/', views.alumni_mentorship, name='alumni_mentorship'),
    path('alumni/internships/', views.alumni_internships, name='alumni_internships'),
    
    # Student URLs
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/alumni/', views.student_alumni_search, name='student_alumni_search'),
    path('student/events/', views.student_events, name='student_events'),
    path('student/mentorship/', views.student_mentorship, name='student_mentorship'),
    path('student/internships/', views.student_internships, name='student_internships'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/alumni/', views.admin_alumni_management, name='admin_alumni_management'),
    path('admin/events/', views.admin_events, name='admin_events'),
    path('admin/funds/', views.admin_funds, name='admin_funds'),
    path('admin/mentorship/', views.admin_mentorship, name='admin_mentorship'),
    
    # Payment URLs
    path('payment/process/<int:donation_id>/', views.payment_process, name='payment_process'),
    path('payment/process/mentorship/<int:mentorship_id>/', views.payment_process, name='payment_process'),
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
]
