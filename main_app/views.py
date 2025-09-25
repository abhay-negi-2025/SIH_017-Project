from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import stripe
from django.conf import settings

from .models import (
    Profile, Alumni, Student, CollegeAdmin, Event, EventRegistration,
    Mentorship, Internship, Donation, MentorshipSession
)
from .forms import (
    UserRegistrationForm, AlumniRegistrationForm, StudentRegistrationForm,
    AdminRegistrationForm, EventForm, MentorshipApplicationForm,
    MentorshipOfferForm, InternshipForm, DonationForm, AlumniSearchForm,
    StudentMentorshipForm
)  

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        from django.contrib.auth.models import User
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, user_type=user_type)
        return JsonResponse({'message': 'User added successfully'})
    return JsonResponse({'message': 'Invalid request'})


def welcome(request):
    """Welcome page with login options"""
    return render(request, 'welcome.html')


def user_login(request):
    """Handle user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                profile = Profile.objects.get(user=user, user_type=user_type)
                login(request, user)
                return redirect('dashboard')
            except Profile.DoesNotExist:
                messages.error(request, 'Invalid user type for this account.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


def user_logout(request):
    """Handle user logout"""
    logout(request)
    return redirect('welcome')


def register(request, user_type):
    """Handle user registration"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            profile = Profile.objects.create(user=user, user_type=user_type)
            
            if user_type == 'alumni':
                alumni_form = AlumniRegistrationForm(request.POST)
                if alumni_form.is_valid():
                    alumni = alumni_form.save(commit=False)
                    alumni.profile = profile
                    alumni.save()
                    messages.success(request, 'Alumni registration successful!')
                    return redirect('login')
            
            elif user_type == 'student':
                student_form = StudentRegistrationForm(request.POST)
                if student_form.is_valid():
                    student = student_form.save(commit=False)
                    student.profile = profile
                    student.save()
                    messages.success(request, 'Student registration successful!')
                    return redirect('login')
            
            elif user_type == 'admin':
                admin_form = AdminRegistrationForm(request.POST)
                if admin_form.is_valid():
                    admin = admin_form.save(commit=False)
                    admin.profile = profile
                    admin.save()
                    messages.success(request, 'Admin registration successful!')
                    return redirect('login')
        
        messages.error(request, 'Registration failed. Please check your information.')
    
    else:
        user_form = UserRegistrationForm()
    
    context = {
        'user_form': user_form,
        'user_type': user_type,
    }
    
    if user_type == 'alumni':
        context['alumni_form'] = AlumniRegistrationForm()
    elif user_type == 'student':
        context['student_form'] = StudentRegistrationForm()
    elif user_type == 'admin':
        context['admin_form'] = AdminRegistrationForm()
    
    return render(request, f'auth/register_{user_type}.html', context)


@login_required
def dashboard(request):
    """Main dashboard - redirects based on user type"""
    try:
        profile = Profile.objects.get(user=request.user)
        
        if profile.user_type == 'alumni':
            return redirect('alumni_dashboard')
        elif profile.user_type == 'student':
            return redirect('student_dashboard')
        elif profile.user_type == 'admin':
            return redirect('admin_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('welcome')
    
    return redirect('welcome')


@login_required
def alumni_dashboard(request):
    """Alumni dashboard"""
    try:
        alumni = Alumni.objects.get(profile__user=request.user)
    except Alumni.DoesNotExist:
        messages.error(request, 'Alumni profile not found.')
        return redirect('welcome')
    
    # Get recent activities
    recent_donations = Donation.objects.filter(donor=alumni).order_by('-donation_date')[:5]
    recent_internships = Internship.objects.filter(posted_by=alumni).order_by('-posted_at')[:5]
    mentorship_sessions = Mentorship.objects.filter(mentor=alumni).order_by('-created_at')[:5]
    
    context = {
        'alumni': alumni,
        'recent_donations': recent_donations,
        'recent_internships': recent_internships,
        'mentorship_sessions': mentorship_sessions,
    }
    
    return render(request, 'alumni/dashboard.html', context)


@login_required
def alumni_search(request):
    """Search alumni by year and branch"""
    form = AlumniSearchForm(request.GET)
    alumni_list = Alumni.objects.all()
    
    if form.is_valid():
        branch = form.cleaned_data.get('branch')
        batch_year = form.cleaned_data.get('batch_year')
        search_query = form.cleaned_data.get('search_query')
        
        if branch:
            alumni_list = alumni_list.filter(branch=branch)
        if batch_year:
            alumni_list = alumni_list.filter(batch_year=batch_year)
        if search_query:
            alumni_list = alumni_list.filter(
                Q(profile__user__first_name__icontains=search_query) |
                Q(profile__user__last_name__icontains=search_query) |
                Q(current_company__icontains=search_query)
            )
    
    context = {
        'form': form,
        'alumni_list': alumni_list,
    }
    
    return render(request, 'alumni/search.html', context)


@login_required
def alumni_donations(request):
    """Alumni donations page"""
    try:
        alumni = Alumni.objects.get(profile__user=request.user)
    except Alumni.DoesNotExist:
        messages.error(request, 'Alumni profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = alumni
            donation.save()
            
            # Here you would integrate with payment gateway
            messages.success(request, 'Donation initiated. Please complete payment.')
            return redirect('payment_process', donation_id=donation.id)
    else:
        form = DonationForm()
    
    # Get donation history
    donations = Donation.objects.filter(donor=alumni).order_by('-donation_date')
    
    context = {
        'form': form,
        'donations': donations,
    }
    
    return render(request, 'alumni/donations.html', context)


@login_required
def alumni_events(request):
    """View and register for events"""
    events = Event.objects.filter(is_active=True, event_date__gte=timezone.now()).order_by('event_date')
    
    # Get user registrations
    user_profile = Profile.objects.get(user=request.user)
    registrations = []
    
    if user_profile.user_type == 'alumni':
        alumni = Alumni.objects.get(profile=user_profile)
        registrations = EventRegistration.objects.filter(alumni=alumni)
    elif user_profile.user_type == 'student':
        student = Student.objects.get(profile=user_profile)
        registrations = EventRegistration.objects.filter(student=student)
    
    context = {
        'events': events,
        'registrations': registrations,
    }
    
    return render(request, 'alumni/events.html', context)


@login_required
def alumni_mentorship(request):
    """Alumni mentorship management"""
    try:
        alumni = Alumni.objects.get(profile__user=request.user)
    except Alumni.DoesNotExist:
        messages.error(request, 'Alumni profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = MentorshipOfferForm(request.POST)
        if form.is_valid():
            mentorship = form.save(commit=False)
            mentorship.mentor = alumni
            mentorship.status = 'pending'
            mentorship.save()
            messages.success(request, 'Mentorship offer created successfully!')
            return redirect('alumni_mentorship')
    else:
        form = MentorshipOfferForm()
    
    # Get mentorship offers and sessions
    mentorship_offers = Mentorship.objects.filter(mentor=alumni).order_by('-created_at')
    
    context = {
        'form': form,
        'mentorship_offers': mentorship_offers,
        'alumni': alumni,
    }
    
    return render(request, 'alumni/mentorship.html', context)


@login_required
def alumni_internships(request):
    """Alumni internship posting"""
    try:
        alumni = Alumni.objects.get(profile__user=request.user)
    except Alumni.DoesNotExist:
        messages.error(request, 'Alumni profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = InternshipForm(request.POST)
        if form.is_valid():
            internship = form.save(commit=False)
            internship.posted_by = alumni
            internship.save()
            messages.success(request, 'Internship posted successfully!')
            return redirect('alumni_internships')
    else:
        form = InternshipForm()
    
    # Get posted internships
    internships = Internship.objects.filter(posted_by=alumni).order_by('-posted_at')
    
    context = {
        'form': form,
        'internships': internships,
    }
    
    return render(request, 'alumni/internships.html', context)


@login_required
def student_dashboard(request):
    """Student dashboard"""
    try:
        student = Student.objects.get(profile__user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('welcome')
    
    # Get student activities
    mentorship_applications = Mentorship.objects.filter(student=student).order_by('-created_at')[:5]
    event_registrations = EventRegistration.objects.filter(student=student).order_by('-registration_date')[:5]
    
    context = {
        'student': student,
        'mentorship_applications': mentorship_applications,
        'event_registrations': event_registrations,
    }
    
    return render(request, 'student/dashboard.html', context)


@login_required
def student_alumni_search(request):
    """Student alumni search (same as alumni search)"""
    return alumni_search(request)


@login_required
def student_events(request):
    """Student events (same as alumni events)"""
    return alumni_events(request)


@login_required
def student_mentorship(request):
    """Student mentorship application"""
    try:
        student = Student.objects.get(profile__user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = StudentMentorshipForm(request.POST)
        if form.is_valid():
            # Find available mentor
            branch = form.cleaned_data['branch']
            available_mentors = Alumni.objects.filter(
                branch=branch, 
                is_mentor=True
            ).exclude(
                mentorship__status='active'
            )[:1]
            
            if available_mentors:
                mentor = available_mentors[0]
                mentorship = Mentorship.objects.create(
                    mentor=mentor,
                    student=student,
                    topic=form.cleaned_data['topic'],
                    description=form.cleaned_data['description'],
                    status='pending'
                )
                messages.success(request, 'Mentorship application submitted! Please complete payment.')
                return redirect('payment_process', mentorship_id=mentorship.id)
            else:
                messages.error(request, 'No available mentors found for your branch.')
    else:
        form = StudentMentorshipForm()
    
    # Get student's mentorship applications
    mentorship_applications = Mentorship.objects.filter(student=student).order_by('-created_at')
    
    context = {
        'form': form,
        'mentorship_applications': mentorship_applications,
    }
    
    return render(request, 'student/mentorship.html', context)


@login_required
def student_internships(request):
    """View available internships"""
    internships = Internship.objects.filter(is_active=True).order_by('-posted_at')
    
    context = {
        'internships': internships,
    }
    
    return render(request, 'student/internships.html', context)


@login_required
def admin_dashboard(request):
    """Admin dashboard"""
    try:
        admin = CollegeAdmin.objects.get(profile__user=request.user)
    except CollegeAdmin.DoesNotExist:
        messages.error(request, 'Admin profile not found.')
        return redirect('welcome')
    
    # Get statistics
    total_alumni = Alumni.objects.count()
    total_students = Student.objects.count()
    total_events = Event.objects.count()
    total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    active_mentorships = Mentorship.objects.filter(status='active').count()
    
    context = {
        'admin': admin,
        'total_alumni': total_alumni,
        'total_students': total_students,
        'total_events': total_events,
        'total_donations': total_donations,
        'active_mentorships': active_mentorships,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_alumni_management(request):
    """Admin alumni management"""
    try:
        admin = CollegeAdmin.objects.get(profile__user=request.user)
    except CollegeAdmin.DoesNotExist:
        messages.error(request, 'Admin profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        # Add new alumni
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            # Create user first
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='defaultpassword123'  # Default password
            )
            
            profile = Profile.objects.create(user=user, user_type='alumni')
            alumni = form.save(commit=False)
            alumni.profile = profile
            alumni.save()
            
            messages.success(request, 'Alumni added successfully!')
            return redirect('admin_alumni_management')
    
    alumni_list = Alumni.objects.all().order_by('-profile__created_at')
    
    context = {
        'alumni_list': alumni_list,
        'admin': admin,
    }
    
    return render(request, 'admin/alumni_management.html', context)


@login_required
def admin_events(request):
    """Admin event management"""
    try:
        admin = CollegeAdmin.objects.get(profile__user=request.user)
    except CollegeAdmin.DoesNotExist:
        messages.error(request, 'Admin profile not found.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = admin
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('admin_events')
    else:
        form = EventForm()
    
    events = Event.objects.all().order_by('-created_at')
    
    context = {
        'form': form,
        'events': events,
    }
    
    return render(request, 'admin/events.html', context)


@login_required
def admin_funds(request):
    """Admin fund tracking"""
    try:
        admin = CollegeAdmin.objects.get(profile__user=request.user)
    except CollegeAdmin.DoesNotExist:
        messages.error(request, 'Admin profile not found.')
        return redirect('welcome')
    
    donations = Donation.objects.all().order_by('-donation_date')
    total_funds = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'donations': donations,
        'total_funds': total_funds,
    }
    
    return render(request, 'admin/funds.html', context)


@login_required
def admin_mentorship(request):
    """Admin mentorship monitoring"""
    try:
        admin = CollegeAdmin.objects.get(profile__user=request.user)
    except CollegeAdmin.DoesNotExist:
        messages.error(request, 'Admin profile not found.')
        return redirect('welcome')
    
    mentorships = Mentorship.objects.all().order_by('-created_at')
    mentorship_stats = Mentorship.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'mentorships': mentorships,
        'mentorship_stats': mentorship_stats,
    }
    
    return render(request, 'admin/mentorship.html', context)


def payment_process(request, donation_id=None, mentorship_id=None):
    """Handle payment processing"""
    if donation_id:
        donation = get_object_or_404(Donation, id=donation_id)
        amount = int(donation.amount * 100)  # Convert to paise
        description = f"Donation: {donation.purpose}"
    elif mentorship_id:
        mentorship = get_object_or_404(Mentorship, id=mentorship_id)
        amount = 10000  # ₹100 in paise
        description = f"Mentorship: {mentorship.topic}"
    else:
        messages.error(request, 'Invalid payment request.')
        return redirect('welcome')
    
    try:
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            description=description,
        )
        
        context = {
            'client_secret': intent.client_secret,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'amount': amount / 100,
            'description': description,
        }
        
        return render(request, 'payment/process.html', context)
    
    except stripe.error.StripeError as e:
        messages.error(request, f'Payment error: {str(e)}')
        return redirect('welcome')


@csrf_exempt
def payment_webhook(request):
    """Handle payment webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Update payment status in database
        # This would need to be implemented based on your payment tracking
        
    return JsonResponse({'status': 'success'})
