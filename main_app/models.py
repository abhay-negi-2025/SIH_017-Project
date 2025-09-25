from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('alumni', 'Alumni'),
        ('student', 'Student'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"


class Alumni(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('AE', 'Aerospace Engineering'),
    ]
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    batch_year = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2030)])
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES)
    cgpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    current_company = models.CharField(max_length=100, blank=True)
    current_position = models.CharField(max_length=100, blank=True)
    work_experience = models.IntegerField(default=0)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    is_mentor = models.BooleanField(default=False)
    mentor_rate_per_student = models.IntegerField(default=100)
    max_students_per_month = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.branch} {self.batch_year}"


class Student(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('AE', 'Aerospace Engineering'),
    ]
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    batch_year = models.IntegerField(validators=[MinValueValidator(2020), MaxValueValidator(2030)])
    branch = models.CharField(max_length=5, choices=BRANCH_CHOICES)
    current_semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    cgpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    college_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.branch} {self.batch_year}"


class CollegeAdmin(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    college_name = models.CharField(max_length=200)
    college_id = models.CharField(max_length=50, unique=True)
    designation = models.CharField(max_length=100, default="Administrator")

    def __str__(self):
        return f"{self.profile.user.get_full_name()} - {self.college_name}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    max_participants = models.IntegerField(default=100)
    created_by = models.ForeignKey(CollegeAdmin, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = [['event', 'alumni'], ['event', 'student']]

    def __str__(self):
        participant = self.alumni or self.student
        return f"{participant} - {self.event.title}"


class Mentorship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    mentor = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    hours_per_month = models.IntegerField(default=10)
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentor} mentoring {self.student} - {self.topic}"


class Internship(models.Model):
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    duration_months = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    stipend = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    location = models.CharField(max_length=200)
    contact_email = models.EmailField()
    posted_by = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class Donation(models.Model):
    donor = models.ForeignKey(Alumni, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=200, default="General Fund")
    payment_id = models.CharField(max_length=100)
    donation_date = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.donor} - ₹{self.amount}"


class MentorshipSession(models.Model):
    mentorship = models.ForeignKey(Mentorship, on_delete=models.CASCADE)
    session_date = models.DateTimeField()
    duration_hours = models.FloatField()
    notes = models.TextField(blank=True)
    mentor_feedback = models.TextField(blank=True)
    student_feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.mentorship} - {self.session_date}"
