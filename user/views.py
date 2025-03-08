from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import SignupForm, LoginForm, EmailAuthenticationForm, PasswordResetRequestForm
from .models import CustomUser, Property
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Sum
import random
from datetime import datetime, timedelta
from django.utils.timezone import now
import json

User = get_user_model()

# Minimum Age for Signup
MIN_AGE = 22

@login_required
def dashboard_view(request):
    if request.user.user_type == 'home owner':
        return homeowner_dashboard(request)
    else:
        # For tenant or other user types
        return render(request, 'user/tenant_dashboard.html')

@login_required
def home_view(request):
    return dashboard_view(request)

@login_required
def homeowner_dashboard(request):
    # Get user's properties
    properties = Property.objects.filter(homeowner=request.user)
    
    # For demonstration purposes, using placeholder data where needed
    # In a real app, you'd calculate these from your database
    context = {
        'properties': properties,
        'property_count': properties.count(),
        'rented_count': 0,  # Replace with actual query when you have booking model
        'available_count': properties.count(),  # Replace with actual calculation
        'total_income': 90000460.00,  # Replace with actual data
        'income_change': -1.5,
        'yesterday_income': 9940.00,
        'last_week_income': 25658.00,
        'total_expenses': 50000660.00,
        'expenses_change': 2.5,
        'yesterday_expenses': 5240.00,
        'last_week_expenses': 22658.00,
        'bookings': [],  # Replace with actual bookings query when you have the model
        'monthly_earnings_data': json.dumps([
            {'month': 'Jan', 'amount': 5000},
            {'month': 'Feb', 'amount': 7000},
            {'month': 'Mar', 'amount': 6500},
            {'month': 'Apr', 'amount': 8000},
            {'month': 'May', 'amount': 9500},
            {'month': 'Jun', 'amount': 10000},
            {'month': 'Jul', 'amount': 11000},
            {'month': 'Aug', 'amount': 9000},
            {'month': 'Sep', 'amount': 12000},
            {'month': 'Oct', 'amount': 13500},
            {'month': 'Nov', 'amount': 15000},
            {'month': 'Dec', 'amount': 16000}
        ])
    }
    
    return render(request, 'user/dashboard.html', context)

@login_required
def property_list(request):
    properties = Property.objects.filter(homeowner=request.user)
    return render(request, 'user/property_list.html', {'properties': properties})

@login_required
def add_property(request):
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        location = request.POST.get('location')
        property_type = request.POST.get('property_type')
        price = request.POST.get('price')
        bedrooms = request.POST.get('bedrooms')
        bathrooms = request.POST.get('bathrooms')
        description = request.POST.get('description')
        
        property = Property(
            homeowner=request.user,
            title=title,
            location=location,
            property_type=property_type,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            description=description
        )
        
        if 'image' in request.FILES:
            property.image = request.FILES['image']
            
        property.save()
        messages.success(request, "Property added successfully!")
        return redirect('property_list')
    
    return render(request, 'user/add_property.html')

@login_required
def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, homeowner=request.user)
    
    if request.method == 'POST':
        # Handle form submission
        property.title = request.POST.get('title')
        property.location = request.POST.get('location')
        property.property_type = request.POST.get('property_type')
        property.price = request.POST.get('price')
        property.bedrooms = request.POST.get('bedrooms')
        property.bathrooms = request.POST.get('bathrooms')
        property.description = request.POST.get('description')
        
        if 'image' in request.FILES:
            property.image = request.FILES['image']
            
        property.save()
        messages.success(request, "Property updated successfully!")
        return redirect('property_list')
    
    return render(request, 'user/edit_property.html', {'property': property})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, homeowner=request.user)
    
    if request.method == 'POST':
        property.delete()
        messages.success(request, "Property deleted successfully!")
        return redirect('property_list')
    
    return render(request, 'user/delete_property.html', {'property': property})

# Placeholder views for other dashboard features
@login_required
def booking_list(request):
    return render(request, 'user/booking_list.html', {'bookings': []})

@login_required
def notifications(request):
    return render(request, 'user/notifications.html')

@login_required
def settings_view(request):
    return render(request, 'user/settings.html')

@login_required
def payment_details(request):
    return render(request, 'user/payment_details.html')

@login_required
def transactions(request):
    return render(request, 'user/transactions.html')

@login_required
def report(request):
    return render(request, 'user/report.html')

# Generate OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Send OTP via Email
def send_otp_email(email, otp):
    subject = "Your OTP for Signup/Login"
    message = f"Your OTP is {otp}. This OTP is valid for 5 minutes."
    from_email = "noreply@yourdomain.com"
    send_mail(subject, message, from_email, [email], fail_silently=False)

# Signup with Age Validation
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Validate Age
            date_of_birth = form.cleaned_data.get('date_of_birth')
            if date_of_birth:
                today = datetime.today().date()
                age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
                if age < MIN_AGE:
                    messages.error(request, "You must be at least 22 years old to sign up.")
                    return render(request, 'user/signup.html', {'form': form})

            user.save()
            messages.success(request, "Your account has been created successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    
    else:
        form = SignupForm()
    
    return render(request, 'user/signup.html', {'form': form})

# OTP Verification for Signup
def verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')
        cached_otp = cache.get(f"otp_{email}")

        if cached_otp and cached_otp == entered_otp:
            signup_data = request.session.get('signup_data')
            if signup_data:
                if 'date_of_birth' in signup_data:
                    signup_data['date_of_birth'] = datetime.fromisoformat(signup_data['date_of_birth']).date()

                user = User.objects.create_user(
                    username=signup_data['username'],
                    email=signup_data['email'],
                    phone_number=signup_data['phone_number'],
                    address=signup_data['address'],
                    company_name=signup_data['company_name'],
                    date_of_birth=signup_data['date_of_birth'],
                    user_type=signup_data['user_type'],
                    password=signup_data['password1'],
                )
                del request.session['signup_data']
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Session expired. Please try signing up again.")
                return redirect('signup')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'user/verify_otp.html')

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

# Login with OTP, but skip OTP if the user has logged in within 3 hours
def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')

        if form.is_valid():
            user = authenticate(request, email=email, password=password)

            if user:
                last_otp_verified_time = cache.get(f"last_otp_verified_{email}")

                # Check if the last OTP verification was within the last 3 hours
                if last_otp_verified_time and (now() - last_otp_verified_time).total_seconds() < 3 * 3600:
                    # Directly log in the user without OTP
                    login(request, user)
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    request.session['user_type'] = user.user_type
                    request.session.set_expiry(3600)  # Session expires in 1 hour

                    messages.success(request, "Login successful!")
                    return redirect('dashboard')

                # Otherwise, generate OTP and ask for verification
                otp = generate_otp()
                cache.set(f"otp_{email}", otp, timeout=300)
                send_otp_email(email, otp)

                request.session['login_email'] = email
                request.session['login_password'] = password

                messages.info(request, f"An OTP has been sent to {email}. Please enter it to complete login.")
                return redirect('login_verify_otp')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def login_verify_otp_view(request):
    if request.method == 'POST':
        email = request.session.get('login_email')
        password = request.session.get('login_password')
        entered_otp = request.POST.get('otp')

        cached_otp = cache.get(f"otp_{email}")

        if cached_otp and cached_otp == entered_otp:
            # Manually fetch the user
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "No account found with this email.")
                return redirect('login')

            # Check if the password is correct
            if user.check_password(password):
                login(request, user)

                # Store session data
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                request.session['user_type'] = user.user_type
                request.session.set_expiry(3600)  # Session expires in 1 hour

                # Store last OTP verification time to bypass OTP for the next 3 hours
                cache.set(f"last_otp_verified_{email}", now(), timeout=3 * 3600)

                messages.success(request, "Login successful!")
                del request.session['login_email']
                del request.session['login_password']
                return redirect('dashboard')  # Redirect to dashboard
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'user/login_verify_otp.html')

# Logout and Clear Session
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')  # Redirect to login page after logout

def landing_page(request):
    return render(request, 'user/landing.html')

def about_page(request):
    return render(request, 'user/about.html')

def service_page(request):
    return render(request, 'user/service.html')

def properties_list(request):
    """View to list all properties with filtering and featured properties."""
    featured_properties = Property.objects.filter(featured=True)  # Featured properties
    all_properties = Property.objects.all()  # All properties

    # Filtering
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if location:
        all_properties = all_properties.filter(location__icontains=location)
    if property_type:
        all_properties = all_properties.filter(property_type=property_type)
    if min_price:
        all_properties = all_properties.filter(price__gte=min_price)
    if max_price:
        all_properties = all_properties.filter(price__lte=max_price)

    return render(request, 'user/properties_list.html', {
        'featured_properties': featured_properties,
        'all_properties': all_properties,
    })

def property_detail(request, pk):
    """View to show details of a single property."""
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'user/property_detail.html', {'property': property})


def view_property_detail(request, pk):
    """View to show details of a single property."""
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'user/view_property.html', {'property': property})

def password_reset_request_view(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_user_model().objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode())

                # Send password reset email
                reset_url = request.build_absolute_uri(f'/reset-password/{uid}/{token}/')

                subject = 'Password Reset Request'
                message = render_to_string('user/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })

                send_mail(subject, message, 'noreply@yourdomain.com', [email])

                messages.success(request, "A password reset link has been sent to your email.")
                return redirect('login')
            except get_user_model().DoesNotExist:
                messages.error(request, "No user found with this email address.")
                return redirect('password_reset_request')
        else:
            messages.error(request, "Please provide a valid email address.")
    else:
        form = PasswordResetRequestForm()

    return render(request, 'user/password_reset_request.html', {'form': form})

def password_reset_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your password has been reset successfully. You can now log in.")
                    return redirect('login')
            else:
                form = SetPasswordForm(user)

            return render(request, 'user/password_reset.html', {'form': form})
        else:
            messages.error(request, "The reset link is invalid or expired.")
            return redirect('password_reset_request')
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        messages.error(request, "The reset link is invalid or expired.")
        return redirect('password_reset_request')