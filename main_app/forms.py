from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Alumni, Student, CollegeAdmin, Event, Mentorship, Internship, Donation


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class AlumniRegistrationForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = ['batch_year', 'branch', 'cgpa', 'current_company', 'current_position', 
                 'work_experience', 'linkedin_profile', 'github_profile', 'is_mentor', 
                 'mentor_rate_per_student', 'max_students_per_month']


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['batch_year', 'branch', 'current_semester', 'cgpa', 'college_name']


class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = CollegeAdmin
        fields = ['college_name', 'college_id', 'designation']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'venue', 'registration_fee', 'max_participants']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class MentorshipApplicationForm(forms.ModelForm):
    class Meta:
        model = Mentorship
        fields = ['topic', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class MentorshipOfferForm(forms.ModelForm):
    class Meta:
        model = Mentorship
        fields = ['topic', 'description', 'hours_per_month']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = ['company_name', 'position', 'description', 'requirements', 
                 'duration_months', 'stipend', 'location', 'contact_email']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'purpose']
        widgets = {
            'purpose': forms.TextInput(attrs={'placeholder': 'e.g., Scholarship Fund, Infrastructure Development'}),
        }


class AlumniSearchForm(forms.Form):
    BRANCH_CHOICES = [
        ('', 'All Branches'),
        ('CSE', 'Computer Science Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('CHE', 'Chemical Engineering'),
        ('AE', 'Aerospace Engineering'),
    ]
    
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, required=False)
    batch_year = forms.IntegerField(required=False, min_value=2000, max_value=2030)
    search_query = forms.CharField(max_length=100, required=False, 
                                 widget=forms.TextInput(attrs={'placeholder': 'Search by name or company'}))


class StudentMentorshipForm(forms.Form):
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
    
    branch = forms.ChoiceField(choices=BRANCH_CHOICES, required=True)
    topic = forms.CharField(max_length=200, required=True, 
                          widget=forms.TextInput(attrs={'placeholder': 'e.g., Machine Learning, Web Development'}))
    description = forms.CharField(required=True, 
                                widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe what you want to learn and your goals'}))
