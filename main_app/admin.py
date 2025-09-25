from django.contrib import admin
from .models import (
    Profile, Alumni, Student, CollegeAdmin, Event, EventRegistration,
    Mentorship, Internship, Donation, MentorshipSession
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'phone', 'created_at']
    list_filter = ['user_type', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ['profile', 'batch_year', 'branch', 'current_company', 'is_mentor']
    list_filter = ['branch', 'batch_year', 'is_mentor']
    search_fields = ['profile__user__username', 'profile__user__email', 'current_company']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'batch_year', 'branch', 'current_semester', 'college_name']
    list_filter = ['branch', 'batch_year', 'college_name']
    search_fields = ['profile__user__username', 'profile__user__email', 'college_name']

@admin.register(CollegeAdmin)
class CollegeAdminAdmin(admin.ModelAdmin):
    list_display = ['profile', 'college_name', 'college_id', 'designation']
    search_fields = ['college_name', 'college_id', 'profile__user__username']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'venue', 'registration_fee', 'created_by', 'is_active']
    list_filter = ['event_date', 'is_active', 'created_by']
    search_fields = ['title', 'venue', 'description']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'get_participant', 'registration_date', 'payment_status']
    list_filter = ['payment_status', 'registration_date']
    
    def get_participant(self, obj):
        return obj.alumni or obj.student
    get_participant.short_description = 'Participant'

@admin.register(Mentorship)
class MentorshipAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'student', 'topic', 'status', 'start_date', 'payment_status']
    list_filter = ['status', 'payment_status', 'start_date']
    search_fields = ['topic', 'description']

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'position', 'duration_months', 'stipend', 'posted_by', 'is_active']
    list_filter = ['duration_months', 'is_active', 'posted_by']
    search_fields = ['company_name', 'position', 'description']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'amount', 'purpose', 'donation_date', 'is_verified']
    list_filter = ['is_verified', 'donation_date']
    search_fields = ['donor__profile__user__username', 'purpose']

@admin.register(MentorshipSession)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = ['mentorship', 'session_date', 'duration_hours']
    list_filter = ['session_date']
    search_fields = ['mentorship__topic']
